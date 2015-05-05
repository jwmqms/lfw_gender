-------------------------------------------------------------------------------
-- File         : tb_fixed_pt_subtractor.vhd
-- Entity       : inv
-- Architecture : tb
-- Author       : James Mnatzaganian
-- Created      : 05/05/15
-- VHDL'93
-------------------------------------------------------------------------------

library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity tb_fixed_pt_subtractor is 
end tb_fixed_pt_subtractor;

architecture tb of tb_fixed_pt_subtractor is
 
	component fixed_pt_subtractor is
		generic( n : integer := 11;
				 m : integer := 1
			   );
		port( A : in  std_logic_vector(m+n+1 downto 1);
			  B : in  std_logic_vector(m+n+1 downto 1);
			  Y : out std_logic_vector(m+n+1 downto 1)
			);
	end component;

signal A : STD_LOGIC_VECTOR(1+4+1 downto 1); -- input
signal B : STD_LOGIC_VECTOR(1+4+1 downto 1); -- input
signal Y : STD_LOGIC_VECTOR(1+4+1 downto 1); -- output

begin
	
	uut: fixed_pt_subtractor
	generic map ( m => 1, n=>4)
	port map    ( A => A,
				  B => B,
				  Y => Y
				);
	
	sim: process
	begin
		
		-- Overflow case
		-- Correct = "0111111111111"
		A <= "0000000000000";		
		B <= "1000000000000";
		wait for 10 ns;
		
		-- 2's comp overflow case
		-- Correct = "0000000000000"
		A <= "0000000000000";		
		B <= "0000000000000";
		wait for 10 ns;
		
		-- Positive - Positive
		-- Correct = "0010000000000"
		A <= "0110101010001";		
		B <= "0100101010001";
		wait for 10 ns;
		
		-- Positive - Negative
		-- Correct = "0111111111111"
		A <= "0110101010001";		
		B <= "1100101010001";
		wait for 10 ns;
		
		-- Negative - Negative
		-- Correct = "0010000000000"
		A <= "1110101010001";		
		B <= "1100101010001";
		wait for 10 ns;
		
		-- Negative - Positive
		-- Correct = "1010000000000"
		A <= "1110101010001";		
		B <= "0100101010001";
		wait for 10 ns;
	end process;
end tb;