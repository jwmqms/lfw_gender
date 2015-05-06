-------------------------------------------------------------------------------
-- File         : inv.vhd
-- Entity       : inv
-- Architecture : behv
-- Author       : James Mnatzaganian
-- Created      : 05/05/15
-- VHDL'93
-------------------------------------------------------------------------------

library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.numeric_std.ALL;

entity inv is
	generic( n : integer := 11;
			 m : integer := 1
		   );
	port( A : in  std_logic_vector(m+n+1 downto 1);
		  Y : out std_logic_vector(m+n+1 downto 1)
		);
end inv;

architecture behv of inv is
	signal max  : std_logic_vector(m+n+1 downto 1);
begin
	-- The maximum value
	max(m+n+1)        <= '0';
	max(m+n downto 1) <= (others => '1');
	
	process(A)
		variable temp : std_logic_vector(m+n+2 downto 1);
		variable one  : std_logic_vector(m+n+2 downto 1);
		variable min  : std_logic_vector(m+n+1 downto 1);
	begin		
		-- The minimum value
		min(m+n+1)        := '1';
		min(m+n downto 1) := (others => '0');
		
		if (A = min) then
			-- Max negative num (only overflow case) so return max positive num
			y <= max;			
		else
			-- The number '1' in fixed point
			one(m+n+2 downto 2) := (others => '0');
			one(1)              := '1';
			
			-- Perform 2's comp
			temp := std_logic_vector(unsigned('0' & not A) + unsigned(one));
			
			Y <= temp(m+n+1 downto 1);
		end if;
	end process;
end behv;