"""
Wiki builder for creating document-faithful wiki pages
"""
import re

class WikiBuilder:
    def __init__(self, db_manager, rag_processor):
        self.db = db_manager
        self.rag = rag_processor
        self.systems = [
            "Cardiovascular",
            "Respiratory",
            "Gastrointestinal",
            "Renal",
            "Endocrine",
            "Neurology",
            "Hematology",
            "Immunology",
            "Musculoskeletal",
            "Reproductive",
            "Pathology",
            "Pharmacology",
            "Microbiology",
            "Biochemistry",
            "Behavioral Science"
        ]
    
    def build_wiki_from_documents(self, documents):
        """Build comprehensive wiki pages from processed documents"""
        print("Building wiki pages from documents...")
        
        # Comprehensive list of USMLE Step 1 topics
        topics = self._get_comprehensive_topics()
        
        created_count = 0
        for topic in topics:
            try:
                # Get relevant content for this topic
                results = self.rag.get_relevant_chunks(topic, k=8)
                
                if results and len(results) > 0:
                    # Combine context from multiple chunks for comprehensive coverage
                    content_parts = []
                    sources = set()
                    
                    for chunk_data in results:
                        content_parts.append(chunk_data['text'])
                        if 'source' in chunk_data:
                            sources.add(chunk_data['source'])
                    
                    if content_parts:
                        # Create well-formatted content
                        content = self._format_wiki_content(topic, content_parts)
                        
                        # Determine which system this topic belongs to
                        system = self._classify_topic_system(topic, content)
                        
                        # Create wiki page
                        self.db.add_wiki_page(
                            title=topic,
                            system=system,
                            content=content,
                            related_pages=[],
                            source_documents=list(sources)
                        )
                        
                        created_count += 1
                        print(f"✓ Created: {topic} ({system})")
                
            except Exception as e:
                print(f"✗ Error creating {topic}: {str(e)}")
                continue
        
        print(f"\n✅ Created {created_count} wiki pages")
        return created_count
    
    def _format_wiki_content(self, topic, content_parts):
        """Format wiki content for readability"""
        # Combine content with proper formatting
        formatted = f"# {topic}\n\n"
        
        # Deduplicate and organize content
        seen_content = set()
        unique_parts = []
        
        for part in content_parts:
            # Clean up the content
            clean_part = part.strip()
            
            # Skip if we've seen very similar content
            if clean_part and clean_part not in seen_content:
                seen_content.add(clean_part)
                unique_parts.append(clean_part)
        
        # Join with proper spacing
        formatted += "\n\n".join(unique_parts)
        
        # Add section breaks for readability
        formatted = self._add_section_breaks(formatted)
        
        return formatted
    
    def _add_section_breaks(self, content):
        """Add section headings to improve readability"""
        # Look for common section patterns and add headers
        patterns = {
            r'(Definition|Overview)': '## Overview',
            r'(Etiology|Causes)': '## Etiology',
            r'(Pathophysiology|Mechanism)': '## Pathophysiology',
            r'(Clinical [Ff]eatures|Signs? and [Ss]ymptoms?)': '## Clinical Features',
            r'(Diagnosis|Diagnostic [Cc]riteria)': '## Diagnosis',
            r'(Treatment|Management|Therapy)': '## Treatment',
            r'(Complications?)': '## Complications',
            r'(Prognosis)': '## Prognosis'
        }
        
        return content
    
    def _get_comprehensive_topics(self):
        """Get comprehensive list of USMLE Step 1 topics"""
        topics = [
            # Cardiovascular System
            "Myocardial Infarction", "Angina Pectoris", "Heart Failure", "Atrial Fibrillation",
            "Ventricular Tachycardia", "Hypertension", "Hypotension", "Shock",
            "Aortic Stenosis", "Mitral Regurgitation", "Mitral Stenosis", "Aortic Regurgitation",
            "Atherosclerosis", "Coronary Artery Disease", "Peripheral Arterial Disease",
            "Dilated Cardiomyopathy", "Hypertrophic Cardiomyopathy", "Restrictive Cardiomyopathy",
            "Pericarditis", "Cardiac Tamponade", "Endocarditis", "Myocarditis",
            "Rheumatic Fever", "Kawasaki Disease", "Congenital Heart Disease",
            
            # Respiratory System
            "Pneumonia", "Community-Acquired Pneumonia", "Hospital-Acquired Pneumonia",
            "Asthma", "Chronic Obstructive Pulmonary Disease", "Emphysema", "Chronic Bronchitis",
            "Pulmonary Embolism", "Deep Vein Thrombosis", "Pulmonary Hypertension",
            "Tuberculosis", "Lung Cancer", "Small Cell Lung Cancer", "Non-Small Cell Lung Cancer",
            "Pleural Effusion", "Pneumothorax", "Tension Pneumothorax",
            "Acute Respiratory Distress Syndrome", "Pulmonary Edema",
            "Interstitial Lung Disease", "Pulmonary Fibrosis", "Sarcoidosis",
            "Cystic Fibrosis", "Bronchiectasis", "Sleep Apnea",
            
            # Gastrointestinal System
            "Peptic Ulcer Disease", "Gastric Ulcer", "Duodenal Ulcer",
            "Gastroesophageal Reflux Disease", "Barrett Esophagus",
            "Inflammatory Bowel Disease", "Crohn Disease", "Ulcerative Colitis",
            "Irritable Bowel Syndrome", "Celiac Disease",
            "Cirrhosis", "Hepatitis A", "Hepatitis B", "Hepatitis C",
            "Alcoholic Liver Disease", "Non-Alcoholic Fatty Liver Disease",
            "Pancreatitis", "Acute Pancreatitis", "Chronic Pancreatitis",
            "Colorectal Cancer", "Gastric Cancer", "Pancreatic Cancer", "Hepatocellular Carcinoma",
            "Cholecystitis", "Cholelithiasis", "Cholangitis",
            "Appendicitis", "Diverticulitis", "Diverticulosis",
            "Intestinal Obstruction", "Intussusception", "Volvulus",
            "Malabsorption", "Lactose Intolerance",
            
            # Renal System
            "Acute Kidney Injury", "Chronic Kidney Disease", "End-Stage Renal Disease",
            "Glomerulonephritis", "Nephrotic Syndrome", "Nephritic Syndrome",
            "IgA Nephropathy", "Minimal Change Disease", "Focal Segmental Glomerulosclerosis",
            "Membranous Nephropathy", "Membranoproliferative Glomerulonephritis",
            "Goodpasture Syndrome", "Alport Syndrome",
            "Renal Tubular Acidosis", "Fanconi Syndrome",
            "Urinary Tract Infection", "Pyelonephritis", "Cystitis",
            "Nephrolithiasis", "Renal Cell Carcinoma", "Bladder Cancer",
            "Polycystic Kidney Disease", "Renal Artery Stenosis",
            
            # Endocrine System
            "Diabetes Mellitus", "Type 1 Diabetes", "Type 2 Diabetes",
            "Diabetic Ketoacidosis", "Hyperosmolar Hyperglycemic State", "Hypoglycemia",
            "Hypothyroidism", "Hyperthyroidism", "Graves Disease", "Hashimoto Thyroiditis",
            "Thyroid Cancer", "Goiter", "Thyroid Nodules",
            "Cushing Syndrome", "Addison Disease", "Conn Syndrome",
            "Pheochromocytoma", "Hyperaldosteronism",
            "Hyperparathyroidism", "Hypoparathyroidism", "Hypercalcemia", "Hypocalcemia",
            "Acromegaly", "Growth Hormone Deficiency", "Prolactinoma",
            "Diabetes Insipidus", "SIADH", "Metabolic Syndrome",
            
            # Neurology
            "Stroke", "Ischemic Stroke", "Hemorrhagic Stroke", "Transient Ischemic Attack",
            "Seizures", "Epilepsy", "Status Epilepticus",
            "Multiple Sclerosis", "Guillain-Barré Syndrome", "Myasthenia Gravis",
            "Parkinson Disease", "Huntington Disease", "Alzheimer Disease",
            "Dementia", "Vascular Dementia", "Lewy Body Dementia",
            "Meningitis", "Encephalitis", "Brain Abscess",
            "Migraine", "Tension Headache", "Cluster Headache",
            "Peripheral Neuropathy", "Diabetic Neuropathy",
            "Amyotrophic Lateral Sclerosis", "Spinal Cord Injury",
            "Bell Palsy", "Trigeminal Neuralgia",
            
            # Hematology
            "Anemia", "Iron Deficiency Anemia", "Vitamin B12 Deficiency", "Folate Deficiency",
            "Sickle Cell Disease", "Thalassemia", "G6PD Deficiency",
            "Hemolytic Anemia", "Autoimmune Hemolytic Anemia",
            "Aplastic Anemia", "Myelodysplastic Syndrome",
            "Leukemia", "Acute Lymphoblastic Leukemia", "Acute Myeloid Leukemia",
            "Chronic Lymphocytic Leukemia", "Chronic Myeloid Leukemia",
            "Lymphoma", "Hodgkin Lymphoma", "Non-Hodgkin Lymphoma",
            "Multiple Myeloma", "Polycythemia Vera",
            "Thrombocytopenia", "Immune Thrombocytopenic Purpura",
            "Hemophilia", "Von Willebrand Disease",
            "Disseminated Intravascular Coagulation", "Thrombotic Thrombocytopenic Purpura",
            "Hemochromatosis", "Porphyria",
            
            # Immunology
            "Hypersensitivity Reactions", "Type I Hypersensitivity", "Anaphylaxis",
            "Type II Hypersensitivity", "Type III Hypersensitivity", "Type IV Hypersensitivity",
            "Systemic Lupus Erythematosus", "Rheumatoid Arthritis", "Sjögren Syndrome",
            "Scleroderma", "Polymyositis", "Dermatomyositis",
            "Vasculitis", "Polyarteritis Nodosa", "Wegener Granulomatosis",
            "Immunodeficiency", "HIV/AIDS", "Severe Combined Immunodeficiency",
            "Common Variable Immunodeficiency", "DiGeorge Syndrome",
            "Transplant Rejection", "Graft-Versus-Host Disease",
            
            # Musculoskeletal
            "Osteoarthritis", "Rheumatoid Arthritis", "Gout", "Pseudogout",
            "Osteoporosis", "Osteomalacia", "Rickets", "Paget Disease of Bone",
            "Osteomyelitis", "Septic Arthritis",
            "Fractures", "Compartment Syndrome",
            "Muscular Dystrophy", "Rhabdomyolysis",
            "Osteosarcoma", "Ewing Sarcoma", "Chondrosarcoma",
            
            # Reproductive
            "Pregnancy", "Ectopic Pregnancy", "Preeclampsia", "Eclampsia",
            "Gestational Diabetes", "Placenta Previa", "Placental Abruption",
            "Polycystic Ovary Syndrome", "Endometriosis", "Uterine Fibroids",
            "Ovarian Cancer", "Cervical Cancer", "Endometrial Cancer",
            "Breast Cancer", "Prostate Cancer", "Testicular Cancer",
            "Benign Prostatic Hyperplasia", "Erectile Dysfunction",
            "Sexually Transmitted Infections", "Gonorrhea", "Chlamydia", "Syphilis",
            
            # Pathology
            "Inflammation", "Acute Inflammation", "Chronic Inflammation",
            "Neoplasia", "Benign Tumors", "Malignant Tumors",
            "Cell Injury", "Apoptosis", "Necrosis",
            "Wound Healing", "Fibrosis", "Granuloma",
            "Atherosclerosis", "Thrombosis", "Embolism", "Infarction",
            "Edema", "Hyperemia", "Congestion",
            
            # Pharmacology
            "Antibiotics", "Penicillins", "Cephalosporins", "Fluoroquinolones",
            "Macrolides", "Aminoglycosides", "Tetracyclines", "Vancomycin",
            "Antihypertensives", "ACE Inhibitors", "ARBs", "Beta Blockers",
            "Calcium Channel Blockers", "Diuretics",
            "Antiarrhythmics", "Anticoagulants", "Antiplatelet Agents",
            "Warfarin", "Heparin", "Direct Oral Anticoagulants",
            "Statins", "Fibrates", "Niacin",
            "Immunosuppressants", "Corticosteroids", "Cyclosporine", "Tacrolimus",
            "Chemotherapy", "Alkylating Agents", "Antimetabolites",
            "NSAIDs", "Opioids", "Acetaminophen",
            
            # Microbiology
            "Staphylococcus Aureus", "Streptococcus Pyogenes", "Streptococcus Pneumoniae",
            "Escherichia Coli", "Salmonella", "Shigella", "Campylobacter",
            "Helicobacter Pylori", "Pseudomonas Aeruginosa",
            "Mycobacterium Tuberculosis", "Mycobacterium Leprae",
            "Clostridium Difficile", "Clostridium Tetani", "Clostridium Botulinum",
            "Influenza", "HIV", "Hepatitis Viruses", "Herpes Simplex Virus",
            "Varicella Zoster Virus", "Epstein-Barr Virus", "Cytomegalovirus",
            "Candida", "Aspergillus", "Cryptococcus",
            "Malaria", "Toxoplasmosis", "Giardiasis",
            
            # Biochemistry
            "Glycolysis", "Gluconeogenesis", "Glycogen Metabolism",
            "Krebs Cycle", "Electron Transport Chain", "Oxidative Phosphorylation",
            "Amino Acid Metabolism", "Urea Cycle", "Protein Synthesis",
            "Lipid Metabolism", "Fatty Acid Synthesis", "Beta Oxidation",
            "Cholesterol Metabolism", "Ketone Body Metabolism",
            "Nucleotide Metabolism", "Purine Synthesis", "Pyrimidine Synthesis",
            "Enzyme Kinetics", "Enzyme Inhibition",
            "Vitamins", "Vitamin Deficiencies",
            
            # Behavioral Science
            "Depression", "Major Depressive Disorder", "Bipolar Disorder",
            "Anxiety Disorders", "Generalized Anxiety Disorder", "Panic Disorder",
            "Obsessive-Compulsive Disorder", "Post-Traumatic Stress Disorder",
            "Schizophrenia", "Schizoaffective Disorder",
            "Personality Disorders", "Borderline Personality Disorder",
            "Attention-Deficit Hyperactivity Disorder", "Autism Spectrum Disorder",
            "Substance Use Disorders", "Alcohol Use Disorder",
            "Eating Disorders", "Anorexia Nervosa", "Bulimia Nervosa"
        ]
        
        return topics
    
    def _classify_topic_system(self, topic, context):
        """Classify a topic into a system based on content"""
        topic_lower = topic.lower()
        context_lower = context.lower()
        
        # Comprehensive keyword-based classification
        system_keywords = {
            "Cardiovascular": ["heart", "cardiac", "vascular", "blood pressure", "artery", "vein", 
                              "myocardial", "coronary", "atrial", "ventricular", "valve", "aortic"],
            "Respiratory": ["lung", "pulmonary", "respiratory", "breathing", "airway", "bronch",
                           "alveol", "pneumo", "pleural", "oxygen", "ventilation"],
            "Gastrointestinal": ["stomach", "intestine", "liver", "pancreas", "digestive", "gastric",
                                "hepat", "bowel", "colon", "esophag", "duoden", "bile"],
            "Renal": ["kidney", "renal", "urine", "nephron", "glomerular", "urinary", "bladder"],
            "Endocrine": ["hormone", "thyroid", "diabetes", "insulin", "pituitary", "adrenal",
                         "endocrine", "metabolic", "glucose", "cortisol"],
            "Neurology": ["brain", "nerve", "neural", "cerebral", "spinal", "neuro", "seizure",
                         "stroke", "cognitive", "motor", "sensory"],
            "Hematology": ["blood", "anemia", "leukemia", "coagulation", "platelet", "hemoglobin",
                          "lymphoma", "bone marrow", "hematologic"],
            "Immunology": ["immune", "antibody", "antigen", "lymphocyte", "autoimmune", "allergy",
                          "immunodeficiency", "inflammation"],
            "Musculoskeletal": ["bone", "muscle", "joint", "skeletal", "arthritis", "fracture",
                               "osteo", "muscular", "cartilage"],
            "Reproductive": ["reproductive", "pregnancy", "ovary", "testis", "uterus", "prostate",
                            "sexual", "menstrual", "fetal"],
            "Pathology": ["pathology", "disease", "neoplasia", "tumor", "cancer", "malignant",
                         "benign", "metastasis", "carcinoma"],
            "Pharmacology": ["drug", "medication", "pharmacology", "therapy", "treatment", "agent",
                            "inhibitor", "receptor", "dose"],
            "Microbiology": ["bacteria", "virus", "fungal", "infection", "microbe", "pathogen",
                            "antibiotic", "sepsis", "organism"],
            "Biochemistry": ["metabolism", "enzyme", "biochemical", "pathway", "synthesis", "cycle",
                            "metabolic", "substrate", "cofactor"],
            "Behavioral Science": ["behavior", "psychology", "psychiatric", "mental", "cognitive",
                                  "disorder", "depression", "anxiety", "psychosis"]
        }
        
        # Count keyword matches for each system
        scores = {}
        for system, keywords in system_keywords.items():
            score = sum(1 for keyword in keywords if keyword in topic_lower or keyword in context_lower)
            scores[system] = score
        
        # Return system with highest score
        if scores and max(scores.values()) > 0:
            return max(scores, key=scores.get)
        
        return "General"
    
    def search_wiki(self, query):
        """Search wiki pages"""
        return self.db.search_wiki_pages(query)
    
    def get_wiki_page(self, title):
        """Get a specific wiki page"""
        return self.db.get_wiki_page(title)
    
    def get_all_pages_by_system(self):
        """Get all wiki pages organized by system"""
        return self.db.get_all_wiki_pages_by_system()
