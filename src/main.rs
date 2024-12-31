// use this neat lib to make large, more easily visible ascii art
use text_to_ascii_art::to_art;

// load in the words from a file
const WORDS: &'static str = include_str!("../2222.txt");

fn main() {
    for (word_index, word) in WORDS.lines().enumerate() {
        // clear the screen and position the cursor at the top right
        // black magic control characters
        print!("{esc}[2J{esc}[1;1H", esc = 27 as char);
        println!("{word_index}/2222");
        // show a word on the terminal
        match to_art(word.to_string(), "standard", 0, 0, 0) {
            Ok(string) => println!("{}", string),
            Err(err) => println!("Error: {}", err),
        }
        // wait 0.6039604 seconds
        std::thread::sleep(std::time::Duration::from_nanos(603_960_400));
    }
}
