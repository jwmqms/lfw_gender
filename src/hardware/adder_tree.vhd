---------------------------------------------------
-- File: adder_tree.vhd
-- Entity: adder_tree
-- Architecture: STRUCT
-- Author: James Mnatzaganian
-- Created: 4/19/14
-- Modified: 4/22/14
-- VHDL'93
-- Description: The following is the entity and
-- architecture for an adder tree.
----------------------------------------------------
--
library IEEE;
use IEEE.std_logic_1164.all;
use ieee.MATH_REAL.ALL;
use work.pkg.ALL;
--
entity adder_tree is 
  generic (
    n  : integer;
    m  : integer;
    NI : integer  -- # of inputs
    );
  port (
    D : in  STD_LOGIC_VECTOR(NI*(m+n+1) downto 1);
    Y : out STD_LOGIC_VECTOR(m+n+1 downto 1)
    );
  constant layers : integer := integer(ceil(log2(real(NI))));
end adder_tree;
-- 
architecture STRUCT of adder_tree is
--
component fixed_pt_adder
  generic ( n, m : integer);
  port ( A, B : in  STD_LOGIC_VECTOR(m+n+1 downto 1);
         Y    : out STD_LOGIC_VECTOR(m+n+1 downto 1));
end component;
--
type d2_array is array (0 to NI-1) of STD_LOGIC_VECTOR(m+n+1 downto 1);
type d3_array is array (0 to layers-1) of d2_array;
--
signal adder_data : d3_array:= (others => (others => (others => '0')));
--
begin
  -- Generate first layer of adders
  l0: if get_ixr(0, NI) generate
      l1: for j in 0 to get_ix(0, NI) - 1 generate
        EVEN_ADDER0: fixed_pt_adder
          generic map ( m => m, n=>n)
          port map (
            A => D((NI-j*2)*(m+n+1) downto (NI-j*2-1)*(m+n+1)+1),
            B => D((NI-j*2-1)*(m+n+1) downto (NI-j*2-2)*(m+n+1)+1),
            Y => adder_data(0)(j)(m+n+1 downto 1));
      end generate;
    end generate;
    l2: if not get_ixr(0, NI) generate
      l3: for j in 0 to get_ix(0, NI) - 1 generate
        ODD_ADDER0: fixed_pt_adder
          generic map ( m => m, n=>n)
          port map (
            A => D((NI-j*2)*(m+n+1) downto (NI-j*2-1)*(m+n+1)+1),
            B => D((NI-j*2-1)*(m+n+1) downto (NI-j*2-2)*(m+n+1)+1),
            Y => adder_data(0)(j)(m+n+1 downto 1));
      end generate;
      adder_data(0)(get_ix(0, NI))(m+n+1 downto 1) <= D(m+n+1 downto 1);
    end generate;
  
  -- Generate all other adders
  l4: for i in 1 to layers-1 generate
    l5: if get_ixr(i, NI) generate
      l6: for j in 0 to get_ix(i, NI) - 1 generate
        EVEN_ADDER1: fixed_pt_adder
          generic map ( m => m, n=>n)
          port map (
            A => adder_data(i-1)(j*2)(m+n+1 downto 1),
            B => adder_data(i-1)(j*2 + 1)(m+n+1 downto 1),
            Y => adder_data(i)(j)(m+n+1 downto 1));
      end generate;
    end generate;
    l7: if not get_ixr(i, NI) generate
      l8: for j in 0 to get_ix(i, NI) - 1 generate
        ODD_ADDER1: fixed_pt_adder
          generic map ( m => m, n=>n)
          port map (
            A => adder_data(i-1)(j*2)(m+n+1 downto 1),
            B => adder_data(i-1)(j*2 + 1)(m+n+1 downto 1),
            Y => adder_data(i)(j)(m+n+1 downto 1));
      end generate;
      adder_data(i)(get_ix(i, NI))(m+n+1 downto 1) <= adder_data(i-1)(get_ix2(i, NI) - 1)(m+n+1 downto 1);
    end generate;
  end generate;
  --
  -- Set output
  Y <= adder_data(layers-1)(0)(m+n+1 downto 1);
  --
end architecture;