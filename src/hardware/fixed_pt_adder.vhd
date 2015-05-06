---------------------------------------------------
-- File: fixed_pt_adder.vhd
-- Entity: fixed_pt_adder
-- Architecture: STRUCT
-- Author: Qutaiba Saleh
-- Created: 4/15/14
-- Modified: 4/15/14
-- VHDL'93
----------------------------------------------------
--
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.numeric_std.ALL;
use IEEE.STD_LOGIC_UNSIGNED.ALL;

entity fixed_pt_adder is
	generic( n: integer;
	         m: integer
	         );
	Port( A    : in   std_logic_vector(m+n+1 downto 1);
	      B    : in   std_logic_vector(m+n+1 downto 1);
	      Y    : out  std_logic_vector(m+n+1 downto 1)
	      );
end fixed_pt_adder;

architecture struct of fixed_pt_adder is 
  
  component adder is
	   generic(  n: integer;
	             m: integer
	           );
	   Port( A : in   std_logic_vector(m+n+1 downto 1);
	         B : in   std_logic_vector(m+n+1 downto 1);
	         Y : out  std_logic_vector(m+n+1 downto 1)
	        );
	end component;
	------------------------------------------------------------------
	component adder_sel is
	   generic( n: integer;
	            m: integer
	           );
	   Port( A    : in   std_logic_vector(m+n+1 downto 1);
	         ma   : in   std_logic;
	         mb   : in   std_logic;
	         Y    : out  std_logic_vector(m+n+1 downto 1)
	        );
	end component;
  -------------------------------------------------------------------
  -------------------------------------------------------------------
  signal ADD : std_logic_vector(m+n+1 downto 1);
begin
  adder_comp : adder 
	   generic map( n => n,
	                m => m
	           )
	   Port map(    A => A,
	                B => B,
	                Y => ADD  
	        );
	
	adder_sel_comp: adder_sel 
	   generic map( n => n,
	                m => m
	            )
	   Port map(    A   => ADD,
	                ma  => A(m+n+1),
	                mb  => B(m+n+1),
	                Y   => Y
	           );
end struct;