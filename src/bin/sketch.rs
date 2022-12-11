#![allow(
    unused_variables,
    dead_code,
    nonstandard_style,
    unused_imports,
    unused_import_braces,
    unused_mut
)]

use std::{
    collections::VecDeque,
    error::Error,
    io::{stdin, stdout},
};

// https://github.com/kenkoooo/competitive-programming-rs/blob/HEAD/src/utils/scanner.rs
pub struct IO<R, W: std::io::Write>(R, std::io::BufWriter<W>);
impl<R: std::io::Read, W: std::io::Write> IO<R, W> {
    pub fn new(r: R, w: W) -> IO<R, W> {
        IO(r, std::io::BufWriter::new(w))
    }
    pub fn write<S: ToString>(&mut self, s: S) {
        use std::io::Write;
        self.1.write_all(s.to_string().as_bytes()).unwrap();
    }
    pub fn read<T: std::str::FromStr>(&mut self) -> T {
        use std::io::Read;
        let buf = self
            .0
            .by_ref()
            .bytes()
            .map(|b| b.unwrap())
            .skip_while(|&b| b == b' ' || b == b'\n' || b == b'\r' || b == b'\t')
            .take_while(|&b| b != b' ' && b != b'\n' && b != b'\r' && b != b'\t')
            .collect::<Vec<_>>();
        unsafe { std::str::from_utf8_unchecked(&buf) }
            .parse()
            .ok()
            .expect("Parse error.")
    }
    pub fn usize0(&mut self) -> usize {
        self.read::<usize>() - 1
    }
    pub fn vec<T: std::str::FromStr>(&mut self, n: usize) -> Vec<T> {
        (0..n).map(|_| self.read()).collect()
    }
    pub fn chars(&mut self) -> Vec<char> {
        self.read::<String>().chars().collect()
    }
}

fn dag_topological_sort(g: &Vec<Vec<usize>>) -> Vec<usize> {
    let n = g.len();
    let mut in_degree = vec![0; n];
    for from in g {
        for &to in from {
            in_degree[to] += 1;
        }
    }
    let mut q: VecDeque<usize> = VecDeque::new();
    for (i, &d) in in_degree.iter().enumerate() {
        if d == 0 {
            q.push_back(i);
        }
    }
    let mut order = Vec::with_capacity(n);
    while let Some(at) = q.pop_front() {
        for &v in &g[at] {
            in_degree[v] -= 1;
            if in_degree[v] == 0 {
                q.push_back(v);
            }
        }
        order.push(at);
    }
    if order.len() != n {
        panic!("Contains loop");
    }
    order
}

fn dag_single_source_path(
    g: &Vec<Vec<usize>>,
    topsort: &[usize],
    start: usize,
    shortest_path: bool,
) -> Vec<Option<i32>> {
    let mut dist = vec![None; g.len()];
    dist[start] = Some(0);

    for &i in topsort {
        if dist[i].is_none() {
            continue;
        }
        for &to in &g[i] {
            let new_dist = dist[i].unwrap() + 1 /* edge.weight */;
            dist[to] = Some(if dist[to].is_none() {
                new_dist
            } else if shortest_path {
                dist[to].unwrap().min(new_dist)
            } else {
                dist[to].unwrap().max(new_dist)
            }
            )
        }
    }
    dist
}

fn main() -> Result<(), Box<dyn Error>> {
    let mut io = IO::new(stdin(), stdout());
    let n: usize = io.read();

    io.write(0);

    Ok(())
}
