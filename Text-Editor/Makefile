# Makefile for Advanced Text Editor

.PHONY: help install uninstall run clean test

help:
	@echo "Advanced Text Editor - Makefile"
	@echo ""
	@echo "Available targets:"
	@echo "  make install       - Install the text editor (user installation)"
	@echo "  make install-sys   - Install system-wide (requires sudo)"
	@echo "  make uninstall     - Uninstall the text editor"
	@echo "  make run          - Run the application directly"
	@echo "  make clean        - Remove generated files"
	@echo "  make executable   - Make app.py executable"
	@echo ""

install:
	@chmod +x install.sh
	@./install.sh

install-sys:
	@chmod +x install.sh
	@sudo ./install.sh

uninstall:
	@chmod +x uninstall.sh
	@./uninstall.sh

run:
	@python3 app.py

executable:
	@chmod +x app.py
	@echo "✓ app.py is now executable"
	@echo "You can run it with: ./app.py"

clean:
	@rm -f *.pyc
	@rm -rf __pycache__
	@rm -rf *.egg-info
	@rm -rf build dist
	@echo "✓ Cleaned generated files"

test:
	@echo "Running basic test..."
	@python3 -c "import app; print('✓ Module imports successfully')"
