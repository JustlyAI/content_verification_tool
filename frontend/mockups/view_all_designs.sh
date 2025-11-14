#!/bin/bash

echo "=========================================="
echo "Content Verification Tool - Design Mockups"
echo "=========================================="
echo ""
echo "Choose a design to view:"
echo ""
echo "1) Design 1: Professional Dashboard"
echo "   - Metrics-driven with data-rich interface"
echo ""
echo "2) Design 2: Split Screen Workflow"
echo "   - Side-by-side with comprehensive results"
echo ""
echo "3) Design 3: Minimalist Cards"
echo "   - Clean and focused card-based layout"
echo ""
echo "4) View all designs info (README)"
echo ""
echo "0) Exit"
echo ""

read -p "Enter your choice (0-4): " choice

case $choice in
  1)
    echo "Launching Design 1..."
    streamlit run design_1_professional_dashboard.py
    ;;
  2)
    echo "Launching Design 2..."
    streamlit run design_2_split_screen.py
    ;;
  3)
    echo "Launching Design 3..."
    streamlit run design_3_minimalist_cards.py
    ;;
  4)
    cat README.md
    ;;
  0)
    echo "Exiting..."
    exit 0
    ;;
  *)
    echo "Invalid choice. Please run again."
    exit 1
    ;;
esac
