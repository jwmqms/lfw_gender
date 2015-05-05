---------------------------------------------------
-- File: adder_sel.vhd
-- Entity: adder_sel
-- Architecture: BEHV
-- Author: Qutaiba Swleh
-- Created: 4/15/14
-- Modified: 4/15/14
-- VHDL'93
-- Description: 
----------------------------------------------------
--
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.numeric_std.ALL;
use IEEE.STD_LOGIC_UNSIGNED.ALL;

entity adder_sel is
	generic( n: integer := 11;
	         m: integer := 1
	         );
	Port( A    : in   std_logic_vector(m+n+1 downto 1);
	      ma   : in   std_logic; -- MSB of first input
	      mb   : in   std_logic; -- MSB of second input
	      Y    : out  std_logic_vector(m+n+1 downto 1)
	      );
end adder_sel;

architecture Behavioral of adder_sel is
  signal overflow  : std_logic_vector(m+n+1 downto 1);  -- save the max positive value = "011.......1"
  signal underflow : std_logic_vector(m+n+1 downto 1); -- save the max negative value = "100.......0"
begin
  overflow(m+n+1)         <= '0';
  overflow(m+n downto 1)  <= (others => '1');    -- overflow  = "0111....1"
  underflow(m+n+1)        <= '1';
  underflow(m+n downto 1) <= (others => '0');    -- underflow = "1000....0"
  Process(A,ma,mb)
		variable AddOrCase  : std_logic ;
	begin
	  AddOrCase := (((NOT ma) AND (NOT mb) AND A(m+n+1)) OR ( ma AND mb AND (NOT A(m+n+1))));
	  if (AddOrCase = '0') then
	    Y <= A;
	  else
	    if (ma = '0') then
	      Y <= overflow;
	    else
	      Y <= underflow;
	    end if;
	  end if;
	end process;
end Behavioral;