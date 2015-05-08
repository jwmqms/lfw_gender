---------------------------------------------------
-- File: LFSR.vhd
-- Entity: LFSR
-- Architecture: Behavioral
-- Author: Qutaiba Saleh
-- Created: 5/5/15
-- Modified: 5/6/15
-- VHDL'93
-- Description: LFSR
----------------------------------------------------
--
LIBRARY ieee;
USE ieee.std_logic_1164.ALL;
--
entity LFSR is 
  generic (
    n  : integer;
    m  : integer
    );
  port (
    clk        : in  std_logic;
    reset_flag : in  std_logic;
	
	LFSR_init  : in  std_logic_vector(m+n downto 1);
	
	LFSR_out   : out std_logic_vector(m+n+1 downto 1)
    );
end LFSR;
-- 
architecture Behavioral of LFSR is
	signal lfsr_reg : std_logic_vector(m+n downto 1):= (others => '0');
begin
  LFSR_out <= lfsr_reg(m+n) & lfsr_reg;
	weight_proc: process(clk,reset_flag)
	begin
		if(reset_flag' event and reset_flag = '1') then
			lfsr_reg <= LFSR_init;
		end if;
		if (clk' event and clk = '1') then 
			if (reset_flag = '1') then
					lfsr_reg <= lfsr_reg(1) & (lfsr_reg(12) xor lfsr_reg(1)) & lfsr_reg(11)& lfsr_reg(10) & (lfsr_reg(9)  xor lfsr_reg(1))
					& lfsr_reg(8) & (lfsr_reg(7) xor lfsr_reg(1)) & lfsr_reg(6) & lfsr_reg(5) & lfsr_reg(4) & lfsr_reg(3) & lfsr_reg(2);
			end if;
		end if;
	end process;
end architecture;