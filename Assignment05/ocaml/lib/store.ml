(* File: store.ml
   Author: Adam Edwards
   Date: 10/2/2026
   Purpose: The OCaml key-value store, built on an immutable map. The
   pure operations are at the top and the file I/O functions (save and
   load) are at the bottom.

   Template: The StringMap module, the store type, set, get, delete,
   and transaction come from the Assignment 05 handout.
   AI Help: Claude helped plan and draft empty, list, add_line, save,
   read_lines, and load. *)

module StringMap = Map.Make (String)

type store = string StringMap.t

let empty : store = StringMap.empty

let set key value store =
  StringMap.add key value store

let get key store =
  StringMap.find_opt key store

let delete key store =
  StringMap.remove key store

let list store =
  StringMap.bindings store

(* use the new store if the operation worked, otherwise keep the original *)
let transaction operation store =
  match operation store with
  | Ok new_store -> new_store
  | Error _ -> store

  
(* turns one "key value" line into an entry in the store *)
let add_line line store =
  match String.index_opt line ' ' with
  | None -> store
  | Some space ->
      let key = String.sub line 0 space in
      let value = String.sub line (space + 1) (String.length line - space - 1) in
      set key value store

(* Everything below does file I/O. These are the functions with side effects. *)

let save filename store =
  let channel = open_out filename in
  StringMap.iter
    (fun key value -> output_string channel (key ^ " " ^ value ^ "\n"))
    store;
  close_out channel

let rec read_lines channel store =
  match In_channel.input_line channel with
  | None -> store
  | Some line -> read_lines channel (add_line line store)

let load filename =
  if Sys.file_exists filename then begin
    let channel = open_in filename in
    let store = read_lines channel empty in
    close_in channel;
    Ok store
  end
  else Error "could not open file"