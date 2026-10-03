(* File: main.ml
   Author: Adam Edwards
   Date: 10/2/2026
   Purpose: Command loop for the OCaml key-value store. A recursive loop
   carries the current store from one command to the next. All console
   I/O is kept in this file.

   Template: The recursive loop idea (loop current_store, then
   loop new_store) comes from the Assignment 05 handout.
   AI Help: Claude helped plan and draft the loop and the pattern
   matching on each command. *)

open Kvstore

let print_pair (key, value) =
  print_endline (key ^ " = " ^ value)

(* the loop carries the current store from one command to the next *)
let rec loop store =
  print_string "> ";
  flush stdout;
  match In_channel.input_line stdin with
  | None -> ()
  | Some line -> (
      match String.split_on_char ' ' (String.trim line) with
      | [ "QUIT" ] -> ()
      | "SET" :: key :: first :: rest ->
          let value = String.concat " " (first :: rest) in
          loop (Store.set key value store)
      | "SET" :: _ ->
          print_endline "usage: SET key value";
          loop store
      | [ "GET"; key ] ->
          (match Store.get key store with
          | Some value -> print_endline value
          | None -> print_endline "key not found");
          loop store
      | [ "DELETE"; key ] ->
          if Store.get key store = None then print_endline "key not found";
          loop (Store.delete key store)
      | [ "LIST" ] ->
          List.iter print_pair (Store.list store);
          loop store
      | [ "SAVE"; filename ] ->
          (try Store.save filename store
           with Sys_error _ -> print_endline "could not open file");
          loop store
      | [ "LOAD"; filename ] ->
          let result = Store.load filename in
          if Result.is_error result then print_endline "could not open file";
          loop (Store.transaction (fun _ -> result) store)
      | [ "" ] -> loop store
      | _ ->
          print_endline "unknown command";
          loop store)

let () = loop Store.empty