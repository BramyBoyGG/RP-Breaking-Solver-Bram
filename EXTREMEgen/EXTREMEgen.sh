#!/bin/bash

# Check if the required number of arguments is provided
if [[ $# -lt 3 ]]; then
    echo "Usage: $0 <topology_type> <seed> <weight_type> [conditional arguments]"
    echo "  Topology types: DQMR, GRID, TREE"
    echo "  Weight types: 1 = [0, 1]  |  2 = not contained"
    echo "  Conditional arguments:"
    echo "    DQMR: <symptoms> <diseases>"
    echo "    GRID: <size>"
    echo "    TREE: <size> <maxchild>"
    exit 1
fi

# Assign positional arguments
topology_type=$1
seed=$2
weight_type=$3

# Validate seed and weight_type
if ! [[ $seed =~ ^[0-9]+$ ]]; then
    echo "Error: Seed must be an integer."
    exit 1
fi

if [[ $weight_type -ne 1 && $weight_type -ne 2 ]]; then
    echo "Error: Weight type must be 1 or 2."
    exit 1
fi

# Handle conditional arguments based on topology type
case $topology_type in
    DQMR)
        if [[ $# -ne 5 ]]; then
            echo "Error: DQMR requires 2 additional integer arguments: <symptoms> <diseases>."
            exit 1
        fi
        symptoms=$4
        diseases=$5

        if ! [[ $symptoms =~ ^[0-9]+$ && $diseases =~ ^[0-9]+$ ]]; then
            echo "Error: Symptoms and diseases must be integers."
            exit 1
        fi

        # "Running with topology DQMR: seed=$seed, weight_type=$weight_type, symptoms=$symptoms, diseases=$diseases"
        ;;
    GRID)
        if [[ $# -ne 4 ]]; then
            echo "Error: GRID requires 1 additional integer argument: <size>."
            exit 1
        fi
        size=$4

        if ! [[ $size =~ ^[0-9]+$ ]]; then
            echo "Error: Size must be an integer."
            exit 1
        fi

        #  "Running with topology GRID: seed=$seed, weight_type=$weight_type, size=$size"
        ;;
    TREE)
        if [[ $# -ne 5 ]]; then
            echo "Error: TREE requires 2 additional integer arguments: <size> <maxchild>."
            exit 1
        fi
        size=$4
        maxchild=$5

        if ! [[ $size =~ ^[0-9]+$ && $maxchild =~ ^[0-9]+$ ]]; then
            echo "Error: Size and maxchild must be integers."
            exit 1
        fi

        # "Running with topology TREE: seed=$seed, weight_type=$weight_type, size=$size, maxchild=$maxchild"
        ;;
    *)
        echo "Error: Invalid topology type. Choices are: DQMR, GRID, TREE."
        exit 1
        ;;
esac

BASE_PATH="/home/delft/cse3000-how-to-break-a-solver/SharpVelvet/generators/bram_generator"

if [[ $topology_type == "DQMR" ]]; then
    python "$BASE_PATH/generate-dqmr_extreme.py" \
    --symptoms "$symptoms" --diseases "$diseases" --seed "$seed" \
    --outdir "$BASE_PATH/wcnf_output_extreme" \
    --outfile temp > /dev/null 2>&1
elif [[ $topology_type == "GRID" ]]; then
    python "$BASE_PATH/generate-grid_extreme.py" \
    --size "$size" --seed "$seed" \
    --outdir "$BASE_PATH/wcnf_output_extreme" \
    --outfile temp > /dev/null 2>&1
elif [[ $topology_type == "TREE" ]]; then
    python "$BASE_PATH/generate-tree_extreme.py" \
    --size "$size" --maxchild "$maxchild" --seed "$seed" \
    --outdir "$BASE_PATH/wcnf_output_extreme" \
    --outfile temp > /dev/null 2>&1
fi

python "$BASE_PATH/generate_wcnf_extreme.py" \
    --outdir "$BASE_PATH/wcnf_output_extreme" \
    --net "$BASE_PATH/wcnf_output_extreme/net/temp.net" \
    --evi "$BASE_PATH/wcnf_output_extreme/evidence/temp.inst" > /dev/null 2>&1

cat "$BASE_PATH/wcnf_output_extreme/wcnf/temp.wcnf"

