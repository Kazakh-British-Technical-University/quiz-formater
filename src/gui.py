from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QPushButton, QLabel, QSpinBox, QCheckBox, QFileDialog,
                            QComboBox, QMessageBox, QApplication)
from PySide6.QtCore import Qt
import sys
from pathlib import Path
import configparser
from src.io_handler import read_questions, save_questions
from src.question_ops import generate_exam_variants
from src.latex_generator import render_latex_with_jinja
from src.pdf_generator import generate_pdf
from src.utils import format_title

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quiz Converter")
        self.setMinimumWidth(600)
        
        # Load configuration
        self.config = self.get_config()
        
        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        # Input file selection
        input_layout = QHBoxLayout()
        self.input_path = self.config['DEFAULT']['input_path']
        input_label = QLabel("Input CSV:")
        self.input_path_label = QLabel(self.input_path)
        input_button = QPushButton("Browse")
        input_button.clicked.connect(self.select_input_file)
        input_layout.addWidget(input_label)
        input_layout.addWidget(self.input_path_label)
        input_layout.addWidget(input_button)
        layout.addLayout(input_layout)
        
        # Number of variants
        variants_layout = QHBoxLayout()
        variants_label = QLabel("Number of variants:")
        self.variants_spin = QSpinBox()
        self.variants_spin.setRange(1, 100)
        self.variants_spin.setValue(int(self.config['DEFAULT']['num_variants']))
        variants_layout.addWidget(variants_label)
        variants_layout.addWidget(self.variants_spin)
        layout.addLayout(variants_layout)
        
        # Max questions per variant
        max_questions_layout = QHBoxLayout()
        max_questions_label = QLabel("Max questions per variant:")
        self.max_questions_spin = QSpinBox()
        self.max_questions_spin.setRange(1, 100)
        self.max_questions_spin.setValue(int(self.config['DEFAULT']['max_questions']))
        max_questions_layout.addWidget(max_questions_label)
        max_questions_layout.addWidget(self.max_questions_spin)
        layout.addLayout(max_questions_layout)
        
        # Output options
        self.generate_pdf_cb = QCheckBox("Generate PDF")
        self.generate_pdf_cb.setChecked(self.config.getboolean('DEFAULT', 'should_generate_pdf'))
        layout.addWidget(self.generate_pdf_cb)
        
        self.generate_csv_cb = QCheckBox("Generate CSV")
        self.generate_csv_cb.setChecked(self.config.getboolean('DEFAULT', 'should_generate_csv'))
        layout.addWidget(self.generate_csv_cb)
        
        # LaTeX engine selection
        engine_layout = QHBoxLayout()
        engine_label = QLabel("LaTeX Engine:")
        self.engine_combo = QComboBox()
        self.engine_combo.addItems(['tectonic', 'pdflatex'])
        self.engine_combo.setCurrentText(self.config['DEFAULT']['engine'])
        engine_layout.addWidget(engine_label)
        engine_layout.addWidget(self.engine_combo)
        layout.addLayout(engine_layout)
        
        # Template selection
        template_layout = QHBoxLayout()
        template_label = QLabel("LaTeX Template:")
        self.template_path = self.config['DEFAULT']['template_path']
        self.template_path_label = QLabel(self.template_path)
        template_button = QPushButton("Browse")
        template_button.clicked.connect(self.select_template_file)
        template_layout.addWidget(template_label)
        template_layout.addWidget(self.template_path_label)
        template_layout.addWidget(template_button)
        layout.addLayout(template_layout)
        
        # Generate button
        generate_button = QPushButton("Generate Variants")
        generate_button.clicked.connect(self.generate_variants)
        layout.addWidget(generate_button)
        
        # Clean button
        clean_button = QPushButton("Clean Output")
        clean_button.clicked.connect(self.clean_output)
        layout.addWidget(clean_button)
        
        # Status bar
        self.statusBar().showMessage("Ready")

    def get_config(self):
        """Get configuration from file or use defaults."""
        config = configparser.ConfigParser()
        config.read_dict({
            'DEFAULT': {
                'input_path': 'data/input/test.csv',
                'output_dir': 'data/output',
                'num_variants': '3',
                'max_questions': '10',
                'should_generate_pdf': 'True',
                'should_generate_csv': 'False',
                'template_path': 'templates/test.tex',
                'engine': 'tectonic'
            }
        })
        
        config_path = Path('config.ini')
        if config_path.exists():
            config.read(config_path)
        
        return config

    def select_input_file(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Select Input CSV",
            str(Path.cwd()),
            "CSV Files (*.csv)"
        )
        if file_name:
            self.input_path = file_name
            self.input_path_label.setText(file_name)

    def select_template_file(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Select LaTeX Template",
            str(Path.cwd()),
            "LaTeX Files (*.tex)"
        )
        if file_name:
            self.template_path = file_name
            self.template_path_label.setText(file_name)

    def generate_variants(self):
        try:
            # Create output directories
            output_dir = Path(self.config['DEFAULT']['output_dir'])
            for subdir in ['csv', 'pdf', 'tex']:
                (output_dir / subdir).mkdir(parents=True, exist_ok=True)
            
            # Read questions and generate variants
            df = read_questions(self.input_path)
            variants = generate_exam_variants(
                df,
                self.variants_spin.value(),
                self.max_questions_spin.value()
            )
            filename = format_title(self.input_path)

            # Process each variant
            for name, v_df in variants.items():
                tex_path = f"{self.config['DEFAULT']['output_dir']}/tex/{filename}_{name}.tex"

                if self.generate_csv_cb.isChecked():
                    save_questions(v_df, f"{self.config['DEFAULT']['output_dir']}/csv/{filename}_{name}.csv")
                
                if self.generate_pdf_cb.isChecked():
                    render_latex_with_jinja(v_df, self.template_path, tex_path, name)
                    generate_pdf(tex_path, self.config, self.engine_combo.currentText())

            QMessageBox.information(self, "Success", "Exam variants created successfully!")
            self.statusBar().showMessage("Generation completed successfully")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
            self.statusBar().showMessage("Error occurred during generation")

    def clean_output(self):
        try:
            output_dir = Path(self.config['DEFAULT']['output_dir'])
            for subdir in ['csv', 'pdf', 'tex']:
                dir_path = output_dir / subdir
                if dir_path.exists():
                    for file in dir_path.glob('*'):
                        file.unlink()
            
            QMessageBox.information(self, "Success", "Output directories cleaned successfully!")
            self.statusBar().showMessage("Cleaning completed successfully")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
            self.statusBar().showMessage("Error occurred during cleaning")

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec()) 