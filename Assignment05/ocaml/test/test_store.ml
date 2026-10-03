(* File: test_store.ml
   Author: Adam Edwards
   Date: 10/2/2026
   Purpose: Alcotest tests for the OCaml store: set, get, delete,
   immutability of the original store, an aborted and a committed
   transaction, and save followed by load.

   Template: Alcotest layout follows Dr. Lewis's OCaml Minute 03
   example. Transaction scenario comes from the Assignment 05 handout.
   AI Help: Claude helped plan and draft the test cases. *)

open Alcotest
open Kvstore

let test_set_and_get () =
  let store = Store.set "name" "Ada" Store.empty in
  check (option string) "set then get returns the value"
    (Some "Ada") (Store.get "name" store);
  let replaced = Store.set "name" "Grace" store in
  check (option string) "set on an existing key replaces the value"
    (Some "Grace") (Store.get "name" replaced);
  check (option string) "get on a missing key returns None"
    None (Store.get "missing" store)

let test_delete () =
  let store = Store.set "name" "Ada" Store.empty in
  let deleted = Store.delete "name" store in
  check (option string) "deleted key is gone"
    None (Store.get "name" deleted)

let test_original_unchanged () =
  let original = Store.set "x" "10" Store.empty in
  let _ = Store.set "x" "20" original in
  check (option string) "set leaves the original store unchanged"
    (Some "10") (Store.get "x" original)

(* both transaction tests start from x = 10 and try to set x 20 and y 30 *)
let test_transaction_abort () =
  let original = Store.set "x" "10" Store.empty in
  let failing_operation store =
    let _ = store |> Store.set "x" "20" |> Store.set "y" "30" in
    Error "aborted"
  in
  let final = Store.transaction failing_operation original in
  check (option string) "aborted transaction keeps x as 10"
    (Some "10") (Store.get "x" final);
  check (option string) "aborted transaction has no y"
    None (Store.get "y" final)

let test_transaction_commit () =
  let original = Store.set "x" "10" Store.empty in
  let working_operation store =
    Ok (store |> Store.set "x" "20" |> Store.set "y" "30")
  in
  let final = Store.transaction working_operation original in
  check (option string) "committed transaction keeps x as 20"
    (Some "20") (Store.get "x" final);
  check (option string) "committed transaction keeps y as 30"
    (Some "30") (Store.get "y" final)

let test_save_and_load () =
  let original =
    Store.empty |> Store.set "name" "Ada" |> Store.set "language" "OCaml"
  in
  Store.save "test_data.txt" original;
  match Store.load "test_data.txt" with
  | Ok loaded ->
      check (list (pair string string)) "save then load rebuilds the same data"
        (Store.list original) (Store.list loaded)
  | Error message -> fail message

let () =
  run "kvstore"
    [
      ( "store",
        [
          test_case "set and get" `Quick test_set_and_get;
          test_case "delete" `Quick test_delete;
          test_case "original unchanged" `Quick test_original_unchanged;
        ] );
      ( "transaction",
        [
          test_case "abort" `Quick test_transaction_abort;
          test_case "commit" `Quick test_transaction_commit;
        ] );
      ( "files", [ test_case "save and load" `Quick test_save_and_load ] );
    ]