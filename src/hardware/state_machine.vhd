---------------------------------------------------
-- File: state_machine.vhd
-- Entity: top
-- Architecture: Behavioral
-- Author: Qutaiba Saleh
-- Created: 5/5/15
-- Modified: 5/5/15
-- VHDL'93
-- Description: state_machine
----------------------------------------------------
--
LIBRARY ieee;
USE ieee.std_logic_1164.ALL;
use IEEE.numeric_std.ALL;
use IEEE.STD_LOGIC_UNSIGNED.ALL;

--
entity state_machine is 
  generic (
	s  : integer -- size of the input image
    );
  port (
    clk        : in  std_logic;
	Mode       : in std_logic_vector(1 downto 0); -- 00: Idle, 01: Reset, 10: Train, 11: Test
	ready      : out std_logic;
	reset_flag : out std_logic;
	train_flag : out std_logic;
	test_flag  : out std_logic
    );
end state_machine;
-- 
architecture Behavioral of state_machine is
---- state signals ------------------------------------------------------
	type State_type is (idle,reset,train,test);
	attribute enum_encoding                  : string;
	attribute enum_encoding of State_type	 : type is "0001 0010 0100 1000";
	signal Next_state                        : State_type := idle;
---- other signals ------------------------------------------------------
-- for more generic implementation the size of counter should consider s
signal counter        : std_logic_vector(8 downto 0):=(others =>'0');  
begin
	state:process(clk)
	begin 
		if(clk' event and clk = '1') then
			case Next_state is
				when idle =>
					case Mode is
						when "01" =>
							Next_state <= reset;
						when "10" =>
							Next_state <= train;
						when "11" =>
							Next_state <= test;
						when others =>
							Next_state <= idle;
					end case;
					
				when reset =>
					if (counter = std_logic_vector(to_unsigned(s*4, 9))) then
						Next_state <= idle;
					else
						Next_state <= reset;
						end if;
				when train =>
					if (Mode = "10") then
						Next_state <= train;
					else
						Next_state <= idle;
					end if;
				when test =>
					if (Mode = "11") then
						Next_state <= test;
					else
						Next_state <= idle;
					end if;
			end case;
		end if;
	end process;
	
	state_output:process(Next_state)
	begin
		case Next_state is 
			when idle =>
				ready      <= '1';
				reset_flag <= '0';
				train_flag <= '0';
				test_flag  <= '0';
			when reset =>
				ready      <= '0';
				reset_flag <= '1';
				train_flag <= '0';
				test_flag  <= '0';
						
			when train =>
				ready      <= '1';
				reset_flag <= '0';
				train_flag <= '1';
				test_flag  <= '0';
				
			when test =>
				ready      <= '1';
				reset_flag <= '0';
				train_flag <= '0';
				test_flag  <= '1';
			when others =>
				ready      <= '0';
				reset_flag <= '0';
				train_flag <= '0';
				test_flag  <= '0';
		end case;
	end process;
------------------------------------------------------------------------------------
----------- counter for reset state ------------------------------------------------
------------------------------------------------------------------------------------
	reset_counter: process(clk)
	begin
		if(clk' event and clk = '1') then
			if (Next_state = reset) then
				counter <= std_logic_vector(unsigned(counter) +1);
			else 
				counter <= (others => '0');
			end if;
		end if;
	end process;

end architecture;