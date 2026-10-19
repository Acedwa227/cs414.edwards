
(*
File: main.ml
Author: Adam Edwards
Date: 10/18/2026
Purpose: Demonstrates the zipper list using integers and strings.
         Shows insertion, movement, and the current focus.
AI Help: Claude assisted with the demo implementation.
         ChatGPT assisted with comments.
*)

open Assignment06.Zipper

let show_option to_string value =
  match value with
  | None -> "None"
  | Some x -> "Some " ^ to_string x

let rec node_to_list list =
  match list with
  | Nil -> []
  | Cons (head, rest) -> head :: node_to_list rest

(* Displays the list, focus, front, and back *)
let show to_string step zipper =
  let items =
    match zipper with
    | Empty -> "(empty)"
    | Zipper { front = before; focus = current; back = after } ->
        let before_items = List.rev (node_to_list before) in
        let after_items = node_to_list after in
        List.map to_string before_items
        @ [ "[" ^ to_string current ^ "]" ]
        @ List.map to_string after_items
        |> String.concat " "
  in
  Printf.printf "%-26s %-18s front=%s back=%s\n" step items
    (show_option to_string (front zipper))
    (show_option to_string (back zipper))

let () =
  (* Integer zipper demonstration *)
  print_endline "=== int zipper ===";
  let z = Empty in
  Printf.printf "empty at start: %b\n" (empty z);
  let z = push_back 3 z in
  show string_of_int "push_back 3" z;
  let z = push_back 4 z in
  show string_of_int "push_back 4" z;
  let z = push_front 2 z in
  show string_of_int "push_front 2" z;
  let z = push_back 5 z in
  show string_of_int "push_back 5" z;
  let z = push_front 1 z in
  show string_of_int "push_front 1" z;
  let z = move_right z in
  show string_of_int "move_right" z;
  let z = move_right z in
  show string_of_int "move_right" z;
  let z = move_right z in
  show string_of_int "move_right (at back edge)" z;
  let z = move_left z |> move_left |> move_left in
  show string_of_int "move_left x3" z;
  let z = move_left z in
show string_of_int "move_left" z;
  let z = move_left z in
  show string_of_int "move_left (at front edge)" z;
  Printf.printf "focus: %s  empty: %b\n"
    (show_option string_of_int (focus z)) (empty z);

  (* String zipper demonstration *)
  print_endline "\n=== string zipper ===";
  let s = Empty |> push_back "b" |> push_front "a" |> push_back "c" in
  show (fun x -> x) "push b, a, c" s;
  let s = move_right s in
  show (fun x -> x) "move_right" s
