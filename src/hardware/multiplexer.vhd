---------------------------------------------------
-- File: multiplexer.vhd
-- Entity: multiplexer
-- Architecture: Behavioral
-- Author: Qutaiba Saleh
-- Created: 5/5/15
-- Modified: 5/5/15
-- VHDL'93
-- Description: multiplexer
----------------------------------------------------
--
LIBRARY ieee;
USE ieee.std_logic_1164.ALL;
--
entity multiplexer is 
  generic (
    m  : integer;
    n  : integer
    );
  port (
	sel : in  std_logic;
	A   : in  std_logic_vector(m+n+1 downto 1);
	B   : in  std_logic_vector(m+n+1 downto 1);
	Y   : out std_logic_vector(m+n+1 downto 1)
    );
end multiplexer;
-- 
architecture Behavioral of multiplexer is
begin
	mux: process(A,B,sel)
	begin
		if (sel = '1') then
			Y <= A;
		else
			Y <= B;
		end if;
	end process;
end architecture;