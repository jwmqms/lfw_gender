---------------------------------------------------
-- File: comparator.vhd
-- Entity: comparator
-- Architecture: Behavioral
-- Author: Qutaiba Saleh
-- Created: 5/6/15
-- Modified: 5/6/15
-- VHDL'93
-- Description: comparator
----------------------------------------------------
--
LIBRARY ieee;
USE ieee.std_logic_1164.ALL;
--
entity comparator is 
  generic (
    n  : integer;
    m  : integer
    );
  port (
    clk          : in  std_logic;
	network_flag : in  std_logic;
	value_in     : in  std_logic_vector(m+n+1 downto 1);
	value_out    : out std_logic:='0'
    );
end comparator;
-- 
architecture Behavioral of comparator is
	-- One register to save the male network value
	signal male_out : std_logic_vector(m+n+1 downto 1):=(others =>'0');
begin
	comparator_proc: process(clk)
	begin
		if (clk' event and clk = '1') then 
			if (network_flag = '1') then
				male_out <= value_in;
			end if;
		end if;
		
		if (male_out <= value_in) then
			value_out <= '1';
		else 
			value_out <= '0';
		end if;
	end process;

end architecture;