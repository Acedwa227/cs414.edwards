(*
 * File:   question2.ml
 * Author: Adam Edwards (with help from ChatGPT)
 * Date: 8/23/2026
 * Purpose:
 * Implement binary tree pruning and level traversal using recursion.
 *)

 type binary_tree =
  | Empty
  | Node of int * binary_tree * binary_tree

 let rec prune tree =
  match tree with
  | Empty -> Empty
  | Node (_, Empty, Empty) -> Empty
  | Node (value, left, right) ->
      Node (value, prune left, prune right)

let test_tree =
  Node (1,
    Node (2, Empty, Empty),
    Node (3, Node (4, Empty, Empty), Empty))

let test_prune = prune test_tree

let level_traversal tree =
  let rec aux queue acc =
    match queue with
    | [] -> List.rev acc
    | Empty :: rest -> aux rest acc
    | Node (value, left, right) :: rest ->
        aux (rest @ [left; right]) (value :: acc)
  in
  aux [tree] []
  