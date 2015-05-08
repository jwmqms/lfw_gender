---------------------------------------------------
-- File: weight _update_block.vhd
-- Entity: weight _update_block
-- Architecture: STRUCT
-- Author: Qutaiba Saleh
-- Created: 5/5/15
-- Modified: 5/6/15
-- VHDL'93
-- Description: weight _update_block
----------------------------------------------------
--
LIBRARY ieee;
USE ieee.std_logic_1164.ALL;
--
entity weight_update_block is 
  generic (
	s  : integer;
    n  : integer;
    m  : integer
    );
  port (
	Label_in         : in  std_logic;
	train_flag       : in  std_logic;
	
	pixel_in         : in  std_logic_vector(s*(m+n+1) downto 1);
	weight_in_male   : in  std_logic_vector(s*(m+n+1) downto 1);
	weight_in_female : in  std_logic_vector(s*(m+n+1) downto 1);
	alpha            : in  std_logic_vector(m+n+1 downto 1);
	
	weight_out       : out std_logic_vector(s*(m+n+1) downto 1)
    );
end weight_update_block;
-- 
architecture STRUCT of weight_update_block is
	-- component of one weight update that updates only one weight 
	component one_weight_update is 
	  generic (
		n  : integer;
		m  : integer
		);
	  port (
		Label_in      : in  std_logic;
		--train_flag    : in  std_logic;
		
		pixel_in      : in  std_logic_vector(m+n+1 downto 1);
		weight_male   : in  std_logic_vector(m+n+1 downto 1);
		weight_female : in  std_logic_vector(m+n+1 downto 1);
		alpha         : in  std_logic_vector(m+n+1 downto 1);
		
		weight_out    : out std_logic_vector(m+n+1 downto 1)
		);
	end component;
begin
	-- Generate weight update units
	weight_up_gen: for i in 1 to s generate
		weight_update: one_weight_update
			generic map (m => m, n => n)
			port map (
				Label_in   => Label_in,
				--train_flag => train_flag,
				
				pixel_in   => pixel_in(i*(m+n+1) downto (i-1)*(m+n+1)+1),
				weight_male  => weight_in_male(i*(m+n+1) downto (i-1)*(m+n+1)+1),
				weight_female  => weight_in_female(i*(m+n+1) downto (i-1)*(m+n+1)+1),
				alpha      => alpha,
				
				weight_out => weight_out(i*(m+n+1) downto (i-1)*(m+n+1)+1)
			);
		end generate;    
	
end architecture;