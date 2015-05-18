---------------------------------------------------
-- File: pkg.vhd
-- PACKAGE!!!!!
-- Author: James Mnatzaganian
-- Created: 4/19/14
-- Modified: 4/19/14
-- VHDL'93
-- Description: POS
----------------------------------------------------
--
library IEEE;
use ieee.std_logic_1164.all;
use ieee.MATH_REAL.ALL;
package pkg is
  function get_ixr (iter : integer; NI : integer) return boolean; -- true == even layer, false == odd layer
  function get_ix (iter : integer; NI : integer) return integer;  -- return even number of input to that layer
  function get_ix2 (iter : integer; NI : integer) return integer;  -- return remaining instead of n_adds
  function pad_user (n : integer) return integer;
  function pad_master (n : integer) return integer;
  function pad_user2 (m : integer) return integer;
end package;
package body pkg is
  function get_ixr (iter : integer; NI : integer) return boolean is
  --
  variable remaining : integer := NI;
  variable n_adds    : integer := 0;
  --
  begin
    for i in 0 to iter loop
     remaining := remaining - n_adds;
     n_adds    := remaining / 2;
   end loop;
   if (remaining mod 2) = 0 then
     return true;
   else 
     return false;
   end if;
  end get_ixr;
  ----------------------------------------------------------------
  ----------------------------------------------------------------
  function get_ix (iter : integer; NI : integer) return integer is
  --
  variable remaining : integer := NI;
  variable n_adds    : integer := 0;
  --
  begin
    for i in 0 to iter loop
     remaining := remaining - n_adds;
     n_adds    := remaining / 2;
   end loop;
   return n_adds;
  end get_ix;
  ----------------------------------------------------------------
  ----------------------------------------------------------------
  function get_ix2 (iter : integer; NI : integer) return integer is
  --
  variable remaining : integer := NI;
  variable n_adds    : integer := 0;
  --
  begin
    for i in 0 to iter loop
     remaining := remaining - n_adds;
     n_adds    := remaining / 2;
   end loop;
   return remaining;
  end get_ix2;
  ----------------------------------------------------------------
  ----------------------------------------------------------------
  function pad_user (n : integer) return integer is
  --
  variable int : integer := 0;
  --
  begin
    if n < 11 then
      int := 11-n;
    end if;
    return int;
  end pad_user;
  function pad_master (n : integer) return integer is
  --
  variable int : integer := 0;
  --
  begin
    if n > 11 then
      int := n-11;
    end if;
    return int;
  end pad_master;
  function pad_user2 (m : integer) return integer is
  --
  variable int : integer := 0;
  --
  begin
    if m < 8 then
      int := 8-m;
    end if;
    return int;
  end pad_user2;
end package body;