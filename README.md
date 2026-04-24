#  Unbiased AI Debugger

An industry-grade platform for detecting, analyzing, and mitigating bias in machine learning datasets and models.

##  Features

### Core Capabilities
- ** Automatic Bias Detection** - Identifies multiple types of bias using industry-standard metrics
- ** Comprehensive Analysis** - Quantifies bias severity with statistical significance testing
- ** Intelligent Explanations** - Provides human-readable explanations of detected biases
- ** Actionable Mitigation** - Offers specific strategies to reduce identified biases
- ** Visual Analytics** - Interactive charts and dashboards for insights
- ** Export & Reporting** - Download detailed reports in multiple formats

### Supported Bias Types
- **Representation Bias** - Uneven distribution of demographic groups
- **Demographic Bias** - Unfair outcome rates between protected groups
- **Model Performance Bias** - Different accuracy across demographic groups
- **Intersectional Bias** - Combined effects of multiple protected attributes

### Fairness Metrics
- Demographic Parity Difference
- Equalized Odds Difference
- Subgroup Performance Analysis
- Statistical Significance Testing (Chi-square)
- Performance Gap Analysis

##  Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup
```bash
# Clone the repository
git clone <repository-url>
cd unbiased-ai-debugger

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

# Install dependencies
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

##  Quick Start

### Running the Application
```bash
# Start the Streamlit application
streamlit run app/streamlit_app.py
```

The application will open in your browser at `http://localhost:8501`

### Using the Platform
1. **Upload Dataset** - Upload your CSV file through the web interface
2. **Auto-Detection** - The system automatically identifies:
   - Target columns (outcome variables)
   - Protected attributes (demographic variables)
   - Task type (classification/regression)
3. **Analysis** - Comprehensive bias analysis is performed automatically
4. **Results** - View detailed reports with explanations and recommendations

##  Dataset Requirements

### Supported Formats
- **CSV files** with headers
- Minimum 2 columns (features + target)
- Recommended minimum 100 rows for statistical significance

### Expected Columns
The system automatically detects:
- **Target Column**: Keywords like `target`, `label`, `outcome`, `approved`, `hired`, etc.
- **Protected Attributes**: Keywords like `gender`, `race`, `age`, `ethnicity`, `religion`, etc.

### Sample Dataset Format
```csv
age,gender,race,income,education,approved
25,Male,White,50000,Bachelors,1
30,Female,Black,35000,Masters,0
22,Male,Hispanic,25000,High School,1
```

##  Architecture

### Project Structure
```
unbiased-ai-debugger/
├── app/
│   └── streamlit_app.py          # Web interface
├── src/
│   ├── core/                    # Core analysis modules
│   │   ├── preprocessing.py      # Data preprocessing
│   │   ├── dataset_bias.py      # Dataset-level bias analysis
│   │   ├── model_bias.py        # Model training and evaluation
│   │   └── metrics.py          # Fairness metrics calculation
│   ├── analysis/                # Analysis modules
│   │   ├── bias_detection.py    # Bias type detection
│   │   ├── severity.py         # Severity scoring
│   │   └── explanation.py      # Bias explanations
│   ├── mitigation/              # Mitigation strategies
│   │   └── suggestions.py      # Recommendation engine
│   └── engine/                 # Main orchestrator
│       └── debugger.py         # Main analysis pipeline
├── requirements.txt            # Dependencies
├── sample_dataset.csv          # Example dataset
└── README.md                  # This file
```

### Technology Stack
- **Frontend**: Streamlit (web interface)
- **Backend**: Python with scientific computing
- **Analysis**: scikit-learn, fairlearn, AIF360
- **Visualization**: Plotly, Matplotlib
- **Data Processing**: Pandas, Polars

##  Analysis Pipeline

### 1. Data Preprocessing
- Load and validate datasets
- Handle missing values
- Create age groups and intersectional features
- Detect target and protected attributes

### 2. Dataset Bias Analysis
- Representation distribution analysis
- Chi-square statistical testing
- Intersectional group analysis

### 3. Model Training & Evaluation
- Train baseline logistic regression model
- Evaluate overall performance metrics
- Analyze subgroup-specific performance

### 4. Fairness Metrics Calculation
- Demographic Parity Difference
- Equalized Odds Difference
- Subgroup performance gaps

### 5. Bias Detection
- Rule-based bias type identification
- Threshold-based severity assessment
- Statistical significance validation

### 6. Explanation Generation
- Human-readable bias explanations
- Evidence-based reasoning
- Impact assessment

### 7. Mitigation Recommendations
- Data-level interventions
- Model-level adjustments
- Post-processing techniques
- Implementation timelines

##  Understanding Results

### Severity Levels
- **Low** (0-0.30): Minor bias issues, monitoring recommended
- **Moderate** (0.30-0.60): Significant bias, mitigation advised
- **High** (0.60-1.00): Severe bias, immediate action required

### Key Metrics
- **Demographic Parity Gap**: Difference in positive outcome rates between groups
- **Equalized Odds Gap**: Difference in true positive/false positive rates
- **Performance Gap**: Difference in accuracy between demographic groups
- **Representation Imbalance**: Uneven distribution of demographic groups

### Recommendations Categories
- **Priority Actions**: Immediate high-impact interventions
- **Data-Level Fixes**: Dataset balancing and preprocessing
- **Model-Level Fixes**: Fairness-aware training techniques
- **Monitoring**: Long-term tracking and validation

##  Advanced Features

### Export Options
- **JSON Reports**: Complete analysis with all technical details
- **CSV Summaries**: Key metrics for spreadsheet analysis
- **Timestamped Files**: Automatic versioning for tracking

### Visual Analytics
- **Performance Charts**: Subgroup-specific accuracy, precision, recall
- **Distribution Plots**: Demographic representation analysis
- **Fairness Comparisons**: Metrics vs industry thresholds
- **Interactive Dashboards**: Real-time exploration

### Session Management
- **Persistent Analysis**: Results maintained across page refreshes
- **Multiple Analyses**: Compare different datasets
- **Progress Tracking**: Step-by-step analysis progress

##  Testing

### Sample Dataset
Use the provided `sample_dataset.csv` to test the system:
```bash
# Upload the sample dataset through the web interface
# Or test programmatically:
python -c "
from src.engine.debugger import BiasDebugger
debugger = BiasDebugger('sample_dataset.csv')
report = debugger.run()
print('Analysis completed successfully!')
"
```

### Unit Tests
```bash
# Run tests (if available)
python -m pytest tests/
```

##  API Reference

### Main Classes

#### BiasDebugger
```python
class BiasDebugger:
    def __init__(self, dataset_path: str):
        """Initialize with path to CSV dataset"""
        
    def run(self) -> dict:
        """Run complete bias analysis pipeline"""
        return {
            "severity_analysis": {...},
            "bias_summary": "...",
            "bias_explanations": [...],
            "mitigation_suggestions": {...},
            "dataset_bias": {...},
            "fairness_metrics": {...},
            "subgroup_performance": {...},
            "detected_biases": [...]
        }
```

### Core Functions

#### Preprocessing
```python
def preprocess_data(path: str) -> tuple:
    """Complete preprocessing pipeline"""
    return df, target, protected, task_type
```

#### Bias Analysis
```python
def dataset_bias_analysis(df: pd.DataFrame, protected_cols: list) -> dict:
    """Analyze dataset-level bias"""
    
def fairness_metrics(y_true, y_pred, sensitive_features) -> dict:
    """Calculate fairness metrics"""
```

##  Limitations & Considerations

### Statistical Requirements
- Minimum sample size for reliable statistical testing
- Assumes independent and identically distributed data
- Requires sufficient representation of all demographic groups

### Bias Types Covered
- Focuses on common bias types in tabular data
- Does not cover all possible bias manifestations
- Complementary to domain-specific bias analysis

### Model Assumptions
- Uses logistic regression as baseline model
- Binary classification focus (multi-class support limited)
- Assumes features are correctly encoded

##  Contributing

### Development Setup
```bash
# Install development dependencies
python -m pip install -r requirements-dev.txt

# Run with development mode
streamlit run app/streamlit_app.py --server.developmentMode true
```

### Code Style
- Follow PEP 8 guidelines
- Use type hints where appropriate
- Document all public functions and classes

##  License

This project is licensed under the MIT License - see LICENSE file for details.

##  Support

### Common Issues
1. **Import Errors**: Ensure all dependencies are installed
2. **Memory Issues**: Use smaller datasets for initial testing
3. **Column Detection**: Check that target/protected columns follow naming conventions

### Getting Help
- Check the sample dataset format
- Review the troubleshooting section
- Ensure dataset meets minimum requirements

##  Roadmap

### Planned Features
- [ ] Support for multi-class classification
- [ ] Time series bias analysis
- [ ] Custom bias metrics
- [ ] Integration with ML pipelines
- [ ] API endpoints for programmatic access
- [ ] Real-time monitoring dashboard

### Enhancements
- [ ] Additional visualization types
- [ ] Export to more formats (PDF, Excel)
- [ ] Comparative analysis between datasets
- [ ] Automated mitigation application


