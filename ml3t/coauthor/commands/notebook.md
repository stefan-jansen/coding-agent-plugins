---
description: "Create and manage Jupyter notebooks for code examples"
argument-hint: "<notebook-name> --chapter N [--template basic|analysis|ml]"
allowed-tools: [Read, Write, Bash]
---

# Notebook Command

Creates Jupyter notebooks for code examples and exercises.

## Implementation

```bash
# Parse arguments
NAME="${1:-example}"
CHAPTER=$(echo "$ARGUMENTS" | grep -oP '(?<=--chapter )\d+')
TEMPLATE=$(echo "$ARGUMENTS" | grep -oP '(?<=--template )\w+' || echo "basic")

if [ -z "$CHAPTER" ]; then
    echo "❌ Chapter required: --chapter N"
    exit 1
fi

CHAPTER_ID=$(printf "%03d" "$CHAPTER")
NOTEBOOK_DIR="code/notebooks/chapter_${CHAPTER_ID}"
mkdir -p "$NOTEBOOK_DIR"

NOTEBOOK_FILE="$NOTEBOOK_DIR/${NAME}.ipynb"

# Create notebook with template
cat > "$NOTEBOOK_FILE" << 'EOF'
{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": ["# $NAME\n", "Chapter $CHAPTER notebook"]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": ["import pandas as pd\n", "import numpy as np\n", "import matplotlib.pyplot as plt"]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
EOF

# Variable substitution
sed -i "s/\$NAME/$NAME/g" "$NOTEBOOK_FILE"
sed -i "s/\$CHAPTER/$CHAPTER/g" "$NOTEBOOK_FILE"

echo "✅ Created notebook: $NOTEBOOK_FILE"
echo "📝 Open with: jupyter notebook $NOTEBOOK_FILE"
```