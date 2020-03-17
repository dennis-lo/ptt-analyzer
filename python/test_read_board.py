import ptt.reader

def test_read_board():
    parsed_content = ptt.reader.read_board('Baseball')

    # Output test result
    print(parsed_content)

if __name__ == '__main__':
    # Execute test_read_board() when executed from CLI directly
    test_read_board()

