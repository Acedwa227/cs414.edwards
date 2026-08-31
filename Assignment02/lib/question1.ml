(*
 * File:   question1.ml
 * Author: Adam Edwards (with help from ChatGPT)
 * Date: 8/31/2026
 * Purpose:
 * Implement operations on rose trees using OCaml.
 * Includes functions for determining tree size, mapping a function
 * over tree elements, and folding values in the tree.
 *)

type 'a rose = Node of 'a * 'a rose list  

let rec size tree =
  match tree with
  | Node (_, children) ->
    1 + List.fold_left (fun total child -> total + size child) 0 children

let rec map fun_to_apply tree =
  match tree with
  | Node (value, children) ->
      Node (fun_to_apply value, List.map (map fun_to_apply) children)

let rec fold combine tree =
  match tree with
  | Node (value, children) ->
      let folded_children = List.map (fold combine) children in
      combine value folded_children