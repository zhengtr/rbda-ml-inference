from detoxify import Detoxify
import torch
import pandas as pd



def main():
    if torch.cuda.is_available():
        device = torch.device('cuda') 
    else:
        device = torch.device('cpu')
    print(f'Using device: {str(device).upper()}.\n')
    
    model = Detoxify('original', device=device)
    test_text = [
        "<p>the solution can be obtained by using the <strong>outputstream</strong> and using <strong>files.",
        "Hey fk you",
        "<p>Dumbass, the solution can be obtained by using the <strong>outputstream</strong> and using <strong>files.",
    ]
    result = model.predict(test_text)
    print(pd.DataFrame(result, index=test_text).round(5))

if __name__ == "__main__":
    main()