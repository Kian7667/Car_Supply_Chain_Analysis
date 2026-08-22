# 0. Setup
- All files run on the latest stable python version `3.14.7`
- `requirements.txt` file is given under additional_files
- `requirements.txt` can be used to install all dependencies needed by the app or the notebooks 

---
# 1. Objective

The task is to reconstruct the supply chain of vehicles produced by OEM1 in 2015 and determine the total logistics distance travelled before the vehicles reach their customers in order to assess the manufacturer's sustainability. The analysis focuses on the engine and gearshift components as well as the corresponding parts installed in these components.

For each relevant vehicle, the logistics routes from the single-part suppliers to the component suppliers, from the component suppliers to the OEM1 production plant, and from the production plant to the responsible distribution center are reconstructed. At the distribution center, the vehicle handover to the customer is assumed to take place. This assumption is made due to the sustainability objective of focusing on logistics stages that can be influenced by the manufacturer. The manufacturer has no influence on the distance between a customer's location and the responsible distribution center. Furthermore, the registration location does not necessarily correspond to the actual customer location, making an estimation of the final delivery route unreliable. Therefore, no additional transportation from the distribution center to the customer location is considered.

Furthermore, it is assumed that each distribution center is located in the state capital corresponding to the customer's state of registration.

---

# 2. Case Study Notebook

- The notebook assumes the **original Data** to be located under `data/IDA SoSe26 - Data/`

### 1.1 Introduction 
 
- The objective is introduced and the strategy for the analysis is briefly explained

### 1.2 Project Setup

- Dependencies and Function definitions are located here

### 1.3 Importing and Exploring the data

- Each relevant dataset is imported, validated and cleaned.
- Relevant data is kept while irrelevant data is dropped immediately (when uncertain about data importance it is kept) 
- Each step is explained in markdown cells

### 1.4 Data Preparation and Route Integration

- The imported data is now prepared and integrated into a specific format in order to prepare the final dataset contruction

### 1.5. Creating Final Dataset

- The final dataset is created and exported in order to use it in the app 

### 1.6. Evaluation and Results

- The final dataset is briefly evaluated with visualisations
- insights are clearly documented
- the main presentation of the insights is done by the app

---

# 3. Case Study app 



-




# AI-gererated logo

- The logo used in the streamlit app was generated using AI (ChatGPT) and is not a real company logo. It was created for demonstration purposes only and does not represent any actual brand or organization.