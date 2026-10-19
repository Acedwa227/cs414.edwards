
(*
File: test_zipper.ml
Author: Adam Edwards
Date: 10/18/2026
Purpose: Tests the zipper operations, movement, boundaries,
         insertion order, and parametric types.
Template: Based on the Alcotest examples from previous assignments.
AI Help: Claude assisted with the test cases.
         ChatGPT assisted with comments.
*)

open Alcotest
open Assignment06.Zipper

(* Creates a list from 1 to 5 with the focus on 1 *)
let one_to_five () =
  Empty |> push_back 1 |> push_back 2 |> push_back 3 |> push_back 4
  |> push_back 5

let test_empty_zipper () =
  check bool "Empty is empty" true (empty Empty);
  check (option int) "focus of Empty is None" None (focus Empty);
  check (option int) "front of Empty is None" None (front Empty);
  check (option int) "back of Empty is None" None (back Empty);
  check bool "move_left on Empty stays empty" true (empty (move_left Empty));
  check bool "move_right on Empty stays empty" true (empty (move_right Empty))

let test_first_push () =
  let by_front = push_front 7 Empty in
  let by_back = push_back 7 Empty in
  check bool "push_front makes it non-empty" false (empty by_front);
  check (option int) "push_front onto Empty sets the focus" (Some 7)
    (focus by_front);
  check (option int) "push_back onto Empty sets the focus" (Some 7)
    (focus by_back);
  check (option int) "one item is the front" (Some 7) (front by_back);
  check (option int) "one item is the back" (Some 7) (back by_back)

let test_push_order () =
  let z = Empty |> push_back 3 |> push_front 2 |> push_back 4 |> push_front 1 in
  check (list int) "items are in order" [ 1; 2; 3; 4 ] (to_list z);
  check (option int) "front is the last item pushed to the front" (Some 1)
    (front z);
  check (option int) "back is the last item pushed to the back" (Some 4)
    (back z);
  check (option int) "pushing does not move the focus" (Some 3) (focus z)

let test_move_right () =
  let z = one_to_five () |> move_right |> move_right in
  check (option int) "two moves right lands on 3" (Some 3) (focus z);
  check (list int) "moving does not change the order" [ 1; 2; 3; 4; 5 ]
    (to_list z);
  check (option int) "front is still 1" (Some 1) (front z);
  check (option int) "back is still 5" (Some 5) (back z)

let test_move_left () =
  let z = one_to_five () |> move_right |> move_right |> move_right in
  let z = move_left z in
  check (option int) "right three then left one lands on 3" (Some 3) (focus z)

let test_edges () =
  let at_front = one_to_five () in
  check (option int) "move_left at the front edge stays on 1" (Some 1)
    (focus (move_left at_front));
  let at_back =
    one_to_five () |> move_right |> move_right |> move_right |> move_right
  in
  check (option int) "four moves right reach 5" (Some 5) (focus at_back);
  check (option int) "move_right at the back edge stays on 5" (Some 5)
    (focus (move_right at_back));
  check (option int) "back is the focus at the back edge" (Some 5)
    (back at_back);
  check (option int) "front is still 1 at the back edge" (Some 1)
    (front at_back)

let test_push_after_moving () =
  let z = one_to_five () |> move_right |> move_right in
  let z = z |> push_front 0 |> push_back 6 in
  check (list int) "pushes go to the ends, not next to the focus"
    [ 0; 1; 2; 3; 4; 5; 6 ] (to_list z);
  check (option int) "focus stays on 3" (Some 3) (focus z)

let test_strings () =
  let z = Empty |> push_back "b" |> push_front "a" |> push_back "c" in
  check (list string) "string zipper keeps order" [ "a"; "b"; "c" ] (to_list z);
  check (option string) "string focus" (Some "b") (focus z);
  check (option string) "string front" (Some "a") (front z);
  check (option string) "string back" (Some "c") (back z)

let () =
  run "Zipper"
    [
      ( "zipper",
        [
          test_case "empty zipper" `Quick test_empty_zipper;
          test_case "first push" `Quick test_first_push;
          test_case "push order" `Quick test_push_order;
          test_case "move right" `Quick test_move_right;
          test_case "move left" `Quick test_move_left;
          test_case "edges" `Quick test_edges;
          test_case "push after moving" `Quick test_push_after_moving;
          test_case "strings" `Quick test_strings;
        ] );
    ]
