
(*
File: main.ml
Author: Adam Edwards
Date: 11/15/2026
Purpose: Counts lines containing a search string. Uses Fun.protect
         to close files and includes tests for Parts B, C, and D.
Usage: dune exec ./main.exe -- ../data
Template: Assignment 08 handout (Parts B1-B3 and Part D, Option 2).
AI Help: Claude (Anthropic) helped with the substring search,
         test cases, and comments.
*)

(* Opens a file and makes sure it closes, even if an exception occurs.
   f must not return ch or keep it for later; it's closed once f ends. *)
let with_input_file path f =
  let ch = open_in path in
  Fun.protect
    ~finally:(fun () ->
      close_in_noerr ch;
      prerr_endline ("[with_input_file] closed " ^ path))
    (fun () ->
      prerr_endline ("[with_input_file] opened " ^ path);
      f ch)

(* Part D: Opens two files and closes both when finished. *)
let with_two_input_files path1 path2 f =
  with_input_file path1 (fun ch1 ->
    with_input_file path2 (fun ch2 ->
      f ch1 ch2))

(* Checks if a string contains the search text. *)
let contains_substring s sub =
  let n = String.length s in
  let m = String.length sub in
  let rec check i =
    if i + m > n then false
    else if String.sub s i m = sub then true
    else check (i + 1)
  in
  check 0

(* Counts matching lines and can simulate a failure for testing. *)
let count_matches_ocaml path needle ?(fail_after_first_line = false) () =
  if String.length needle = 0 then
    raise (Invalid_argument "search string must not be empty");
  with_input_file path (fun ch ->
    let rec loop count =
      match input_line ch with
      | line ->
        let count' =
          if contains_substring line needle then count + 1 else count
        in
        if fail_after_first_line then
          raise (Failure "simulated failure");
        loop count'
      | exception End_of_file -> count
    in
    loop 0)

(* Counts all lines in a file for the Part D tests. *)
let count_lines ch =
  let rec loop count =
    match input_line ch with
    | _ -> loop (count + 1)
    | exception End_of_file -> count
  in
  loop 0

(* Converts exceptions into messages for the test results. *)
let describe_exn e =
  match e with
  | Failure msg -> "Failure: " ^ msg
  | Invalid_argument msg -> "Invalid_argument: " ^ msg
  | Sys_error msg -> "Sys_error: " ^ msg
  | _ -> Printexc.to_string e

(* Runs tests T1-T7. *)
let run_test name path needle fail expected =
  print_endline "";
  print_endline (name ^ ": path=" ^ path ^ " needle=\"" ^ needle ^ "\""
                 ^ " fail=" ^ string_of_bool fail);
  print_endline ("  expected: " ^ expected);
  match count_matches_ocaml path needle ~fail_after_first_line:fail () with
  | result -> print_endline ("  result:   returned " ^ string_of_int result)
  | exception e -> print_endline ("  result:   exception: " ^ describe_exn e)

(* Part D: Tests opening and counting two files. *)
let run_two_file_test name path1 path2 expected =
  print_endline "";
  print_endline (name ^ ": path1=" ^ path1 ^ " path2=" ^ path2);
  print_endline ("  expected: " ^ expected);
  match with_two_input_files path1 path2
          (fun ch1 ch2 -> (count_lines ch1, count_lines ch2)) with
  | (lines1, lines2) ->
    print_endline ("  result:   returned (" ^ string_of_int lines1 ^ ", "
                   ^ string_of_int lines2 ^ ")")
  | exception e -> print_endline ("  result:   exception: " ^ describe_exn e)

(* Part D: Tests cleanup when an exception occurs. *)
let run_two_file_failure_test name path1 path2 expected =
  print_endline "";
  print_endline (name ^ ": path1=" ^ path1 ^ " path2=" ^ path2
                 ^ " (callback raises)");
  print_endline ("  expected: " ^ expected);
  match with_two_input_files path1 path2
          (fun _ _ -> raise (Failure "simulated failure")) with
  | () -> print_endline "  result:   returned ()"
  | exception e -> print_endline ("  result:   exception: " ^ describe_exn e)

let () =
  if Array.length Sys.argv < 2 then begin
    prerr_endline "usage: main.exe <data folder>";
    exit 1
  end;
  let data = Sys.argv.(1) in
  let sample = data ^ "/sample.txt" in

  run_test "T1" sample "red" false "return 2; close file";
  run_test "T2" sample "orange" false "return 0; close file";
  run_test "T3" (data ^ "/empty.txt") "red" false "return 0; close file";
  run_test "T4" (data ^ "/missing.txt") "red" false
    "opening failure; nothing to release";
  run_test "T5" sample "red" true "exception; close file";
  run_test "T6" sample "" false "rejected before opening file";
  run_test "T7" (data ^ "/long_line.txt") "red" false "return 1; close file";

  run_two_file_test "D1" sample (data ^ "/long_line.txt")
    "return (4, 1); close both files";
  run_two_file_test "D2" sample (data ^ "/missing.txt")
    "second open fails; first file still closes";
  run_two_file_failure_test "D3" sample (data ^ "/long_line.txt")
    "exception; close file 2, then file 1"
