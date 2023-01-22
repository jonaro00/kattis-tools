use graph::*;
mod graph {
    use std::collections::VecDeque;
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
}
