#!/bin/bash

echo "=================================="
echo "      GROMACS ANALYSIS MENU       "
echo "=================================="
echo ""
echo "1) Run gyrate.sh"
echo "2) Run kde.sh"
echo "3) Run hbond.sh"
echo "4) Exit"
echo ""

read -p "Choose an option: " choice

case $choice in

    1)
        echo ""
        echo "Running gyrate.sh..."
        bash gyrate.sh
        ;;

    2)
        echo ""
        echo "Running kde.sh..."
        bash kde.sh
        ;;

    3)
       echo ""
       echo "Running hbond.sh"
       bash hbond.sh
       ;;

    4)
        echo ""
        echo "Exit."
        exit 0
        ;;

    *)
        echo ""
        echo "Invalid option."
        ;;

esac

