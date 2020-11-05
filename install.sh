#! /bin/sh

echo "Installing current.py to ~/scripts/qt..."
cp temp.py current.py &&
  cp current.py ~/scripts/qt &&
    echo "Installation complete!" ||
      echo "Installation failed."
