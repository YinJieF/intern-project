# 1. load data
# 2. build_model
# 3. train_model
# 4. save_model
# 5. evaluate_model
# keras == 2.15.0 / newest

import metrics
import modeling
import data_preprocess

def training(table_id = 'criminal_data_inorder', size = 100):
    # Load data
    train_data, test_data = data_preprocess.load_data('intern-project-415606', 'Criminal_Dataset', table_id, size)

    # Build model (modify the parameter upon change of dataset)
    ner_model = modeling.NERModel(num_tags=6, vocab_size=20000, maxlen=512, embed_dim=32, num_heads=2, ff_dim=32)
    # Train model (compile and fit)
    ner_model.compile(optimizer="adam", loss=modeling.CustomNonPaddingTokenLoss())
    ner_model.fit(train_data, epochs=3)

    #save model
    filepath_model = "./resources/trained_model/ner_model.keras"
    modeling.save_model(ner_model, filepath_model)
    print("Model is saved in " + filepath_model)

    # Evaluate model
    filepath_result = "./resources/model_evaluate/evaluation_result.txt"
    mapping = data_preprocess.make_tag_lookup_table()
    metrics.evaluate_model(ner_model, test_data, mapping, filepath_result)
    print("Model evaluation result is saved in " + filepath_result)

    return filepath_model, filepath_result
