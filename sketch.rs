#![allow(unused_variables, dead_code, nonstandard_style)]

use std::{
    error::Error,
    io::{stdin, BufRead}, vec::IntoIter,
};

fn lines() -> IntoIter<String> {
    stdin()
        .lock()
        .lines()
        .map(|l| l.unwrap())
        .collect::<Vec<String>>()
        .into_iter()
}
fn int(s: String) -> i64 {
    s.parse().unwrap()
}

fn main() -> Result<(), Box<dyn Error>> {
    let mut l = lines();
    l.next().unwrap();

    println!("{}");

    Ok(())
}
