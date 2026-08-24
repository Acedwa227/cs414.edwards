(*
 * File:   question3.ml
 * Author: Adam Edwards (with help from ChatGPT)
 * Date: 8/23/2026
 * Purpose:
 * Implement a general tree type with traversal, height, and insertion functions.
 *)

type general_tree =
  | Empty
  | Node of int list * general_tree list

let rec height tree =
  match tree with
  | Empty -> 0
  | Node (_, children) ->
      1 + List.fold_left (fun max_height child ->
        max max_height (height child)) 0 children

let preorder visit tree =
  let rec traverse tree =
    match tree with
    | Empty -> ()
    | Node (keys, children) ->
        List.iter visit keys;
        List.iter traverse children
  in
  traverse tree

let postorder visit tree =
  let rec traverse tree =
    match tree with
    | Empty -> ()
    | Node (keys, children) ->
        List.iter traverse children;
        List.iter visit keys
  in
  traverse tree

let inorder visit tree =
  let rec traverse tree =
    match tree with
    | Empty -> ()
    | Node (keys, children) ->
        let rec walk keys children =
          match (keys, children) with
          | [], [] -> ()
          | [], child :: rest ->
              traverse child;
              List.iter traverse rest
          | key :: rest_keys, child :: rest_children ->
              traverse child;
              visit key;
              walk rest_keys rest_children
          | _ -> ()
        in
        walk keys children
  in
  traverse tree

let rec insert tree value =
  match tree with
  | Empty -> Node ([value], [Empty; Empty])
  | Node (keys, children) ->
      let rec find_position index = function
        | [] -> index
        | key :: rest ->
            if value < key then index
            else find_position (index + 1) rest
      in
      let position = find_position 0 keys in

      let rec update_child index children =
        match children with
        | [] -> []
        | child :: rest ->
            if index = 0 then
              insert child value :: rest
            else
              child :: update_child (index - 1) rest
      in

      Node (keys, update_child position children)

let test_tree =
  Node (
    [10; 20],
    [
      Node ([5], [Empty; Empty]);
      Node ([15], [Empty; Empty]);
      Node ([25], [Empty; Empty])
    ]
  )

let test_height = height test_tree
let test_insert = insert test_tree 12