
(*
File: zipper.ml
Author: Adam Edwards
Date: 10/18/2026
Purpose: Implements a bidirectional zipper list using
         parametric types and pattern matching.
Template: Based on the list type in Assignment 06.
AI Help: Claude assisted with the zipper implementation.
         ChatGPT assisted with comments.
*)

(* List type from Assignment 06 *)
type 'a node =
  | Nil
  | Cons of 'a * 'a node

(* Represents an empty or non-empty zipper *)
type 'a zipper =
  | Empty
  | Zipper of { front : 'a node; focus : 'a; back : 'a node }

(* Adds an item to the end of a list *)
let rec add_to_end x list =
  match list with
  | Nil -> Cons (x, Nil)
  | Cons (head, rest) -> Cons (head, add_to_end x rest)

(* Returns the last item, or None if empty *)
let rec last list =
  match list with
  | Nil -> None
  | Cons (head, Nil) -> Some head
  | Cons (_, rest) -> last rest

(* Checks if the zipper is empty *)
let empty zipper =
  match zipper with
  | Empty -> true
  | Zipper _ -> false

(* Moves the focus one position left *)
let move_left zipper =
  match zipper with
  | Empty -> Empty
  | Zipper { front = Nil; _ } -> zipper
  | Zipper { front = Cons (x, rest); focus; back } ->
      Zipper { front = rest; focus = x; back = Cons (focus, back) }

(* Moves the focus one position right *)
let move_right zipper =
  match zipper with
  | Empty -> Empty
  | Zipper { back = Nil; _ } -> zipper
  | Zipper { front; focus; back = Cons (x, rest) } ->
      Zipper { front = Cons (focus, front); focus = x; back = rest }

(* Adds an item to the front of the zipper *)
let push_front x zipper =
  match zipper with
  | Empty -> Zipper { front = Nil; focus = x; back = Nil }
  | Zipper { front; focus; back } ->
      Zipper { front = add_to_end x front; focus; back }

(* Adds an item to the back of the zipper *)
let push_back x zipper =
  match zipper with
  | Empty -> Zipper { front = Nil; focus = x; back = Nil }
  | Zipper { front; focus; back } ->
      Zipper { front; focus; back = add_to_end x back }

(* Returns the first item, or None if empty *)
let front zipper =
  match zipper with
  | Empty -> None
  | Zipper { front = Nil; focus; _ } -> Some focus
  | Zipper { front; _ } -> last front

(* Returns the last item, or None if empty *)
let back zipper =
  match zipper with
  | Empty -> None
  | Zipper { back = Nil; focus; _ } -> Some focus
  | Zipper { back; _ } -> last back

(* Returns the current focus, or None if empty *)
let focus zipper =
  match zipper with
  | Empty -> None
  | Zipper { focus; _ } -> Some focus

(* Converts the zipper to a regular list for testing *)
let to_list zipper =
  let rec to_built_in list =
    match list with
    | Nil -> []
    | Cons (head, rest) -> head :: to_built_in rest
  in
  match zipper with
  | Empty -> []
  | Zipper { front; focus; back } ->
      List.rev (to_built_in front) @ (focus :: to_built_in back)
