from connector import NOTION
from data import get_test_data, get_LeetCode_data
import argparse 

if __name__ == "__main__":    
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--url", type=str, help="LeetCode page URL"
    )
    parser.add_argument(
        "--debug", action="store_true", help="create test page on current date"
    )

    args = parser.parse_args()
    Connector = NOTION()

    if args.debug:
        test_data, context = get_test_data()
        Connector.create_page(test_data, context)
    
    else:
        url = args.url
        LeetCode_data, context = get_LeetCode_data(url)
        Connector.create_page(LeetCode_data, context)

