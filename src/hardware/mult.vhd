---------------------------------------------------
-- File: mult.vhd
-- Entity: mult
-- Architecture: BEHV
-- Author: James Mnatzaganian
-- Created: 4/15/14
-- Modified: 4/15/14
-- VHDL'93
-- Description: The following is the entity and
-- architecture for a fixed point multiplier
----------------------------------------------------
--
LIBRARY ieee;
USE ieee.std_logic_1164.ALL;
USE ieee.numeric_std.ALL;
--
entity mult is
  generic ( m : integer;
            n : integer);
  port (
    x, y : in STD_LOGIC_VECTOR(m+n+1 downto 1);
    z    : out STD_LOGIC_VECTOR(m+n+1 downto 1)
    );
end mult;
-- 
architecture BEHV of mult is
--
begin
  process(x, y)
    variable temp : STD_LOGIC_VECTOR(2 * (m + n + 1) downto 1) := (others => '0');
  begin
      temp := STD_LOGIC_VECTOR(signed(x) * signed(y));
      z <= temp(m + 2*n + 1 downto n + 1 );
  end process;
end architecture;