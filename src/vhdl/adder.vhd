---------------------------------------------------
-- File: adder.vhd
-- Entity: adder
-- Architecture: BEHV
-- Author: Qutaiba Saleh
-- Created: 4/15/14
-- Modified: 4/15/14
-- VHDL'93
----------------------------------------------------
--
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.numeric_std.ALL;
use IEEE.STD_LOGIC_UNSIGNED.ALL;

entity adder is
	generic( n: integer := 11;
	         m: integer := 1
	         );
	Port( A : in   std_logic_vector(m+n+1 downto 1);
	      B : in   std_logic_vector(m+n+1 downto 1);
	      Y : out  std_logic_vector(m+n+1 downto 1)
	      );
end adder;

architecture Behavioral of adder is

begin
  Process(A,B)
		variable SY : std_logic_vector(m+n+2 downto 1);
	begin
	  SY  := std_logic_vector( unsigned('0' & A) + unsigned('0' & B));
	  Y   <= SY(m+n+1 downto 1);
	end process;
end Behavioral;