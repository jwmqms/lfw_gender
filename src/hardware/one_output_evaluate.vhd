---------------------------------------------------
-- File: one_weight_update.vhd
-- Entity: one_output_evaluate
-- Architecture: STRUCT
-- Author: Qutaiba Saleh
-- Created: 5/5/15
-- Modified: 5/6/15
-- VHDL'93
-- Description: one_output_evaluate
----------------------------------------------------
--
LIBRARY ieee;
USE ieee.std_logic_1164.ALL;
--
entity one_output_evaluate is 
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
end one_output_evaluate;
-- 
architecture STRUCT of one_output_evaluate is
-- fixed point subtracter component
	component fixed_pt_subtractor is
	generic( n : integer;
			 m : integer
			 );
	port( A : in  std_logic_vector(m+n+1 downto 1);
		  B : in  std_logic_vector(m+n+1 downto 1);
		  Y : out std_logic_vector(m+n+1 downto 1)
		);
end component;
	-- fixed point added component
	component fixed_pt_adder is
	generic( n: integer;
	         m: integer
	         );
	Port( A    : in   std_logic_vector(m+n+1 downto 1);
	      B    : in   std_logic_vector(m+n+1 downto 1);
	      Y    : out  std_logic_vector(m+n+1 downto 1)
	      );
	end component;
	-- multiplication component
	component mult is
	  generic ( m : integer;
				n : integer );
	  port (
		x, y : in STD_LOGIC_VECTOR((m + n) - 1 downto 0);
		z    : out STD_LOGIC_VECTOR((m + n) - 1 downto 0)
		);
	end component;
	-- multiplexer component
	component multiplexer is 
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
	end component;
-------------- connection signals -----------------------------------------------
signal weight_in  : std_logic_vector(m+n+1 downto 1);
signal diff       : std_logic_vector(m+n+1 downto 1);
signal scaled     : std_logic_vector(m+n+1 downto 1);
signal s_pixel_in : std_logic_vector(m+n+1 downto 1);
begin
	multiplexer_comp_w : multiplexer
		generic map (m => m, n => n)
		port map (
			sel => network_flag,
			A   => weight_male,
			B   => weight_female,
			Y   => weight_in
		);
	multiplexer_comp_p : multiplexer
		generic map (m => m, n => n)
		port map (
			sel => test_flag,
			A   => pixel_in,
			B   => zeros,
			Y   => s_pixel_in
		);
	sub : fixed_pt_subtractor
		generic map (n => n, m => m)
		port map (
			A   => weight_in,
			B   => s_pixel_in,
			Y   => diff
		);
		
	mulsc : mult
		generic map (m => m, n => n)
		port map (
			x   => diff,
			y   => scale_in,
			z   => scaled
		);
	mulsq : mult
		generic map (n => n, m => m)
		port map (
			x   => scaled,
			y   => scaled,
			z   => value_out
		);
	
end architecture;