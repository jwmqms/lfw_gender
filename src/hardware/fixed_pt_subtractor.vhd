-------------------------------------------------------------------------------
-- File         : fixed_pt_subtractor.vhd
-- Entity       : inv
-- Architecture : struct
-- Author       : James Mnatzaganian
-- Created      : 05/05/15
-- VHDL'93
-------------------------------------------------------------------------------

library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity fixed_pt_subtractor is
	generic( n : integer := 11;
			 m : integer := 1
		   );
	port( A : in  std_logic_vector(m+n+1 downto 1);
		  B : in  std_logic_vector(m+n+1 downto 1);
		  Y : out std_logic_vector(m+n+1 downto 1)
		);
end fixed_pt_subtractor;

architecture struct of fixed_pt_subtractor is

	component inv is
		generic( n : integer := 11;
			 m : integer := 1
		   );
		port( A : in  std_logic_vector(m+n+1 downto 1);
			  Y : out std_logic_vector(m+n+1 downto 1)
			);
	end component;
	
	component fixed_pt_adder is
		generic( n : integer := 11;
			 m : integer := 1
		   );
		port( A : in  std_logic_vector(m+n+1 downto 1);
			  B : in  std_logic_vector(m+n+1 downto 1);
			  Y : out std_logic_vector(m+n+1 downto 1)
			);
	end component;
	
	signal SUB : std_logic_vector(m+n+1 downto 1);

begin
	invertor : inv
		generic map( n => n,
					 m => m
				   )
		port map   ( A => B,
					 Y => SUB
				   );
	
	adder : fixed_pt_adder
		generic map( n => n,
					 m => m
				   )
		port map   ( A => A,
					 B => SUB,
					 Y => Y
				   );
end struct;