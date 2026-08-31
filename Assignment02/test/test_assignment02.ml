open Assignment02

let test_tree =
  Question1.Node
    (5,
     [
       Question1.Node (10, [Question1.Node (12, [])]);
       Question1.Node (20, []);
     ])

let () =
  Printf.printf "Tree size: %d\n" (Question1.size test_tree)

let mapped_tree = Question1.map (fun x -> x + 1) test_tree

let () =
  match mapped_tree with
  | Question1.Node
      ( root,
        [
          Question1.Node (left, [Question1.Node (left_child, [])]);
          Question1.Node (right, []);
        ] ) ->
      Printf.printf "Mapped values: %d %d %d %d\n"
        root left left_child right
  | _ ->
      Printf.printf "Unexpected tree structure\n"

let sum =
  Question1.fold
    (fun value child_results ->
      value + List.fold_left ( + ) 0 child_results)
    test_tree

let () =
  Printf.printf "Fold sum: %d\n" sum