---------------------------------------------------
-- File: one_weight_update.vhd
-- Entity: one_weight_update
-- Architecture: STRUCT
-- Author: Qutaiba Saleh
-- Created: 5/5/15
-- Modified: 5/6/15
-- VHDL'93
-- Description: one_weight_update
----------------------------------------------------
--
LIBRARY ieee;
USE ieee.std_logic_1164.ALL;
--
entity one_weight_update is 
  generic (
    n  : integer;
    m  : integer
    );
  port (
	clk 		  : in std_logic;
	Label_in      : in  std_logic;
	train_flag    : in  std_logic;
	
	pixel_in      : in  std_logic_vector(m+n+1 downto 1);
	weight_male   : in  std_logic_vector(m+n+1 downto 1);
	weight_female : in  std_logic_vector(m+n+1 downto 1);
	alpha         : in  std_logic_vector(m+n+1 downto 1);
	zeros  		  : in  std_logic_vector(m+n+1 downto 1);
	male_weight_out    : out std_logic_vector(m+n+1 downto 1);
	female_weight_out    : out std_logic_vector(m+n+1 downto 1)
    );
end one_weight_update;
-- 
architecture STRUCT of one_weight_update is
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
signal delta_w    : std_logic_vector(m+n+1 downto 1);
signal s_pixel_in : std_logic_vector(m+n+1 downto 1);
signal s_weight_out: std_logic_vector(m+n+1 downto 1);
signal s_male_weight_out: std_logic_vector(m+n+1 downto 1);
signal s_female_weight_out: std_logic_vector(m+n+1 downto 1);
begin
	male_weight_out <= s_male_weight_out;
	female_weight_out <= s_female_weight_out;
	inv: process(clk)
	begin
		--if (clk' event and clk = '1') then
			if (Label_in = '1') then
				s_male_weight_out <= s_weight_out;
				s_female_weight_out <= s_female_weight_out;
			else
				s_female_weight_out <= s_weight_out;
				s_male_weight_out <= s_male_weight_out;
			end if;
		--end if;
	end process;
	multiplexer_comp_w : multiplexer
		generic map (m => m, n => n)
		port map (
			sel => Label_in,
			A   => weight_male,
			B   => weight_female,
			Y   => weight_in
		);
	multiplexer_comp_p : multiplexer
		generic map (m => m, n => n)
		port map (
			sel => train_flag,
			A   => pixel_in,
			B   => zeros,
			Y   => s_pixel_in
		);
	sub : fixed_pt_subtractor
		generic map (n => n, m => m)
		port map (
			A   => s_pixel_in,
			B   => weight_in,
			Y   => diff
		);
		
	mul : mult
		generic map (m => m, n => n)
		port map (
			x   => diff,
			y   => alpha,
			z   => delta_w
		);
	adder : fixed_pt_adder
		generic map (n => n, m => m)
		port map (
			A   => delta_w,
			B   => weight_in,
			Y   => s_weight_out
		);
		
end architecture;