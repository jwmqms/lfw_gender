---------------------------------------------------
-- File: network_sel.vhd
-- Entity: network_sel
-- Architecture: Behavioral
-- Author: Qutaiba Saleh
-- Created: 5/6/15
-- Modified: 5/6/15
-- VHDL'93
-- Description: network_sel
----------------------------------------------------
--
LIBRARY ieee;
USE ieee.std_logic_1164.ALL;
use ieee.numeric_std.all;
--
entity network_sel is 
  generic (
    n  : integer;
    m  : integer;
	s  : integer;
	l  : integer
    );
  port (
    clk           : in  std_logic;
	test_flag     : in  std_logic;
	pixel_in      : in  std_logic_vector(s*(m+n+1) downto 1);
	netowrk_flag  : out std_logic
    );
end network_sel;
-- 
architecture Behavioral of network_sel is
signal internal_flag : std_logic := '0';
signal counter       : std_logic_vector(l downto 0):= not std_logic_vector(to_unsigned(1, l+1));
--counter(l downto 1) = '1';
--counter(0) = '0';
begin
  netowrk_flag <= counter(l);
	event_proc: process(pixel_in)
	
	begin
		if(pixel_in' event and test_flag = '1' and counter(l) = '1') then
			internal_flag <= '1';
		else
			internal_flag <= '0';
		end if;
	end process;
	
	count_proc: process(clk)
	begin
		if(clk' event and clk = '1') then
			if(test_flag = '1') then
				if (internal_flag = '1') then 
					counter <= counter (l-1 downto 0) & counter(l);
				end if;
			else 
				counter <= not std_logic_vector(to_unsigned(1, l+1));
			end if;
		end if;
	end process;
end architecture;



















