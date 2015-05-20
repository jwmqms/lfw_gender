---------------------------------------------------
-- File: output_evaluate_block.vhd
-- Entity: output_evaluate_block
-- Architecture: STRUCT
-- Author: Qutaiba Saleh
-- Created: 5/5/15
-- Modified: 5/6/15
-- VHDL'93
-- Description: output_evaluate_block
----------------------------------------------------
--
LIBRARY ieee;
USE ieee.std_logic_1164.ALL;
--
entity output_evaluate_block is 
  generic (
	s  : integer;
    n  : integer;
    m  : integer
    );
  port (
	test_flag     : in  std_logic;
	network_flag  : in  std_logic;
	pixel_in      : in  std_logic_vector(s*(m+n+1) downto 1);
	weight_male   : in  std_logic_vector(s*(m+n+1) downto 1);
	weight_female : in  std_logic_vector(s*(m+n+1) downto 1);
	value_out     : out std_logic_vector(m+n+1 downto 1)
    );
end output_evaluate_block;
-- 
architecture STRUCT of output_evaluate_block is
	-- Save Scale value into a register
	signal scale: std_logic_vector(m+n+1 downto 1):= "0000100100100";
	signal s_zeros : std_logic_vector(m+n+1 downto 1):= (others =>'0');
	-- component of one weight update that updates only one weight 
	component one_output_evaluate is 
	  generic (
		n  : integer;
		m  : integer
		);
	  port (
		test_flag     : in  std_logic;
		network_flag  : in  std_logic;
		pixel_in      : in  std_logic_vector(m+n+1 downto 1);
		weight_male   : in  std_logic_vector(m+n+1 downto 1);
		weight_female : in  std_logic_vector(m+n+1 downto 1);
		scale_in      : in  std_logic_vector(m+n+1 downto 1);
		zeros 		  : in  std_logic_vector(m+n+1 downto 1);
		value_out     : out std_logic_vector(m+n+1 downto 1)
		);

	end component;
	-- Add the output of all output evaluate units. This component has only on vector output that will be 
	-- compared to the output of the other network (cluster).
	component adder_tree is 
	  generic (
		n  : integer;
		m  : integer;
		NI : integer  -- # of inputs
		);
	  port (
		D : in  STD_LOGIC_VECTOR(NI*(m+n+1) downto 1);
		Y : out STD_LOGIC_VECTOR(m+n+1 downto 1)
		);
	end component;
----------------- signal that connect the output of weight update units and the adder tree ------
	signal connection : std_logic_vector(s*(m+n+1) downto 1);
begin
	-- Generate weight update units
	out_gen: for i in 1 to s generate
		output_evaluate_one: one_output_evaluate
			generic map (m => m, n => n)
			port map (
				test_flag      => test_flag,
				network_flag   => network_flag,
				pixel_in       => pixel_in(i*(m+n+1) downto (i-1)*(m+n+1)+1),
				weight_male    => weight_male(i*(m+n+1) downto (i-1)*(m+n+1)+1),
				weight_female  => weight_female(i*(m+n+1) downto (i-1)*(m+n+1)+1),
				scale_in       => scale,
				zeros          => s_zeros,
				value_out      => connection(i*(m+n+1) downto (i-1)*(m+n+1)+1)
			);
		end generate;    
		
		adder_tree_comp: adder_tree 
		  generic map ( n => n, m => m, NI => s)
		  port map(
			D => connection,
			Y => value_out
			);	
end architecture;