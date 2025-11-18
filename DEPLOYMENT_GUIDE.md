# Quick Deployment Guide - Step by Step

## Before You Start

### Download the Dataset
1. Go to: https://www.kaggle.com/datasets/fedesoriano/heart-failure-prediction
2. Download `heart.csv`
3. Place it in the project folder (same directory as notebook)

---

## Local Development

### Step 1: Run the Notebook (Google Colab)
Since you're using Colab:
1. Upload `MLZoomcamp.ipynb` to Google Colab
2. Upload `heart.csv` to Colab (or mount Google Drive)
3. Run all cells to train models and generate visualizations
4. Download `heart_disease_model.pkl` from Colab

### Step 2: Train Model Locally (Optional)
```bash
python train.py
```
This creates `heart_disease_model.pkl`

---

## Docker Deployment (Docker Toolbox)

### Step 1: Start Docker Machine
```bash
docker-machine start default
docker-machine env default
eval $(docker-machine env default)
```

### Step 2: Check Docker Machine IP
```bash
docker-machine ip default
```
Note this IP address (e.g., 192.168.99.100)

### Step 3: Build Docker Image
```bash
docker build -t heart-disease-prediction .
```

This may take 5-10 minutes for the first build.

### Step 4: Run Docker Container
```bash
docker run -it --rm -p 9696:9696 heart-disease-prediction
```

### Step 5: Test the Service
Open a new terminal and test:
```bash
# Replace 192.168.99.100 with your Docker Machine IP
curl -X POST http://192.168.99.100:9696/health
```

Full prediction test:
```bash
curl -X POST http://192.168.99.100:9696/predict \
  -H "Content-Type: application/json" \
  -d '{
    "Age": 52,
    "Sex": "M",
    "ChestPainType": "ASY",
    "RestingBP": 120,
    "Cholesterol": 280,
    "FastingBS": 0,
    "RestingECG": "Normal",
    "MaxHR": 150,
    "ExerciseAngina": "N",
    "Oldpeak": 2.5,
    "ST_Slope": "Flat"
  }'
```

---

## Troubleshooting

### Issue: Docker build fails
**Solution:**
- Make sure you have enough disk space
- Try: `docker system prune -a` to clean up
- Rebuild: `docker build -t heart-disease-prediction .`

### Issue: Can't connect to Docker service
**Solution for Docker Toolbox:**
```bash
docker-machine restart default
eval $(docker-machine env default)
```

### Issue: Port 9696 already in use
**Solution:**
```bash
# Use a different port
docker run -it --rm -p 8080:9696 heart-disease-prediction
# Then access via port 8080
```

### Issue: Model file not found
**Solution:**
- Make sure `heart_disease_model.pkl` exists
- Run `python train.py` first
- Or download from Colab after running notebook

---

## Verification Checklist

Before submission, verify:

- [ ] `notebook.ipynb` has clear problem description at the top
- [ ] `notebook.ipynb` shows EDA with visualizations
- [ ] `notebook.ipynb` shows multiple models trained
- [ ] `notebook.ipynb` shows hyperparameter tuning
- [ ] `heart.csv` dataset is accessible (or download instructions in README)
- [ ] `train.py` script exists and can be run
- [ ] `predict.py` Flask service exists
- [ ] `requirements.txt` exists with all dependencies
- [ ] `Pipfile` exists
- [ ] `Dockerfile` exists
- [ ] `README.md` has complete instructions
- [ ] Docker image builds successfully
- [ ] Docker container runs and responds to requests
- [ ] API returns predictions correctly

---

## Quick Commands Reference

### Python Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

### Train Model
```bash
python train.py
```

### Run Service Locally
```bash
python predict.py
```

### Docker Commands
```bash
# Build
docker build -t heart-disease-prediction .

# Run
docker run -it --rm -p 9696:9696 heart-disease-prediction

# Stop all containers
docker stop $(docker ps -aq)

# Remove all containers
docker rm $(docker ps -aq)

# View logs
docker logs <container-id>
```

### Test API
```bash
# Health check
curl http://localhost:9696/health

# Or with Docker Machine IP
curl http://192.168.99.100:9696/health

# Test prediction
python test_api.py
```

---

## Expected Results

### Training Output
- Training accuracy: ~87-90%
- Validation accuracy: ~85-88%
- Test accuracy: ~85-90%
- ROC-AUC: ~90-95%

### API Response Example
```json
{
  "heart_disease_probability": 0.7854,
  "heart_disease": true,
  "risk_level": "High",
  "message": "High risk of heart disease. Seek immediate medical attention."
}
```

---

## Final Notes

1. **For Colab Users**: After running the notebook in Colab, download the `.pkl` file and place it in your local project directory before Docker deployment.

2. **For Docker Toolbox**: Always use the Docker Machine IP (not localhost) when testing.

3. **Time Management**: 
   - Notebook EDA: ~30 minutes to run
   - Model training: ~10-20 minutes
   - Docker build: ~5-10 minutes
   - Total: ~1 hour for complete setup

4. **Common Mistakes to Avoid**:
   - Forgetting to download the model from Colab
   - Using localhost instead of Docker Machine IP
   - Not activating virtual environment
   - Missing dataset file

Good luck with your project! 🚀
