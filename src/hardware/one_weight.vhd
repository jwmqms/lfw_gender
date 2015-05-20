---------------------------------------------------
-- File: one_weight.vhd
-- Entity: one_weight
-- Architecture: Behavioral
-- Author: Qutaiba Saleh
-- Created: 5/5/15
-- Modified: 5/6/15
-- VHDL'93
-- Description: one_weight
----------------------------------------------------
--
LIBRARY ieee;
USE ieee.std_logic_1164.ALL;
--
entity one_weight is 
  generic (
    n  : integer;
    m  : integer
    );
  port (
    clk        		 : in  std_logic;
	Label_in   		 : in  std_logic;
    reset_flag 		 : in  std_logic;
	train_flag 		 : in  std_logic;
	test_flag  		 : in  std_logic;
	
	LFSR_in    		 : in  std_logic_vector(m+n+1 downto 1);
	train_in   		 : in  std_logic_vector(m+n+1 downto 1);
	
	LFSR_out    	 : out std_logic_vector(m+n+1 downto 1);
	weight_train_out : out std_logic_vector(m+n+1 downto 1);
	weight_test_out  : out std_logic_vector(m+n+1 downto 1)
    );
end one_weight;
-- 
architecture Behavioral of one_weight is
	-- Define the weigh register. This register should be the only one in this entity
	signal weight : std_logic_vector(m+n+1 downto 1):=(others =>'0');
begin
	weight_proc: process(clk)
	variable flags_conc : std_logic_vector(2 downto 0);
	begin
	  flags_conc := (reset_flag & train_flag & test_flag);
		if (clk' event and clk = '1') then 
			case flags_conc is
				-- reset
				when "100" =>
					LFSR_out  <= weight;
					weight <= LFSR_in;
					weight_train_out <= weight;--(others => '0');
					weight_test_out <= weight;--(others => '0');
				-- train
				when "010" =>
					LFSR_out  <= (others => '0');
					weight_test_out <= weight;--(others => '0');
					weight_train_out <= weight;
					--if (Label_in = '1') then
						weight <= train_in;
					--end if;
				-- test
				when "001" =>
					LFSR_out  <= (others => '0');
					weight_train_out <= (others => '0');
					weight_test_out <= weight;	
				when others =>
					LFSR_out  <= (others => '0');
					weight_train_out <= weight;--(others => '0');
					weight_test_out <= weight;--(others => '0');
			end case;
		end if;
	end process;

end architecture;