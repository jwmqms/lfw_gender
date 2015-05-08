---------------------------------------------------
-- File: tb_adder_tree.vhd
-- Entity: tb_fixed_pt_adder
-- Architecture: STRUCT
-- Author: Qutaiba Saleh
-- Created: 4/15/14
-- Modified: 4/15/14
-- VHDL'93
-- Testbench for adder tree 
----------------------------------------------------
--
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.numeric_std.ALL;
use IEEE.STD_LOGIC_UNSIGNED.ALL;
--
entity tb_adder_tree is 
  generic( m  : integer := 4; 
           n  : integer := 7; 
           NI : integer := 10);
end tb_adder_tree;

architecture STRUCT of tb_adder_tree is 
--
-- unit under test component decleration 
component adder_tree is 
  generic (
    n  : integer;
    m  : integer;
    NI : integer   -- # of inputs
    );
  port (
    D : in  STD_LOGIC_VECTOR(NI*(m+n+1) downto 1);
    Y : out STD_LOGIC_VECTOR(m+n+1 downto 1)
    );
  end component;
--
-- signals 
signal D  : STD_LOGIC_VECTOR(NI*(m+n+1) downto 1); -- input
signal Y  : STD_LOGIC_VECTOR(m+n+1 downto 1); -- output
signal v1 : STD_LOGIC_VECTOR(m+n+1 downto 1):= (others =>'0');
signal v2 : STD_LOGIC_VECTOR(m+n+1 downto 1):= (others => '0');
signal v3 : STD_LOGIC_VECTOR(m+n+1 downto 1):= (others => '0');
signal v4 : STD_LOGIC_VECTOR(m+n+1 downto 1):= (others => '0');
signal v5 : STD_LOGIC_VECTOR(m+n+1 downto 1):= (others => '0');
signal v6 : STD_LOGIC_VECTOR(m+n+1 downto 1):= (others => '0');
signal v7 : STD_LOGIC_VECTOR(m+n+1 downto 1):= (others => '0');
signal v8 : STD_LOGIC_VECTOR(m+n+1 downto 1):= (others => '0');
signal v9 : STD_LOGIC_VECTOR(m+n+1 downto 1):= (others => '0');
signal v10 : STD_LOGIC_VECTOR(m+n+1 downto 1):= (others => '0');
--
begin
  --
  -- instantiate the unit under test 
  uut: adder_tree
    generic map ( m => m, n=>n, NI=>NI)
    port map (
      D  => D,
      Y  => Y);
  --
  stim_proc: process
   begin		
 
    D <= (others => '0');
    v1(m+n+1 downto 1) <= "111110000000";
    v2(m+n+1 downto 1) <= "000000001001";
    v3(m+n+1 downto 1) <= "000010000000";
    v4(m+n+1 downto 1) <= "111111001000";
    v5(m+n+1 downto 1) <= "111110110000";
    v6(m+n+1 downto 1) <= "000010000000";
    v7(m+n+1 downto 1) <= "111110000000";
    v8(m+n+1 downto 1) <= "000000001001";
    v9(m+n+1 downto 1) <= "111110000000";
    v10(m+n+1 downto 1) <= "000000111001";
    
    wait for 10 ns;
		D(NI*(m+n+1) downto (NI -1)*(m+n+1) + 1) <= v1(m+n+1 downto 1);		
		--wait for 10 ns;
		D((NI -1)*(m+n+1) downto (NI -2)*(m+n+1) + 1) <= v2(m+n+1 downto 1);	
	  --wait for 10 ns;
		D((NI -2)*(m+n+1) downto (NI -3)*(m+n+1) + 1) <= v3(m+n+1 downto 1);		
		--wait for 10 ns;	
		D((NI -3)*(m+n+1) downto (NI -4)*(m+n+1) + 1) <= v4(m+n+1 downto 1);	
		--wait for 10 ns;
		D((NI -4)*(m+n+1) downto (NI -5)*(m+n+1) + 1) <= v5(m+n+1 downto 1);	
		--wait for 10 ns;
		D((NI -5)*(m+n+1) downto (NI -6)*(m+n+1) + 1) <= v6(m+n+1 downto 1);	
		--wait for 10 ns;
		D((NI -6)*(m+n+1) downto (NI -7)*(m+n+1) + 1) <= v7(m+n+1 downto 1);	
		--wait for 10 ns;
		D((NI -7)*(m+n+1) downto (NI -8)*(m+n+1) + 1) <= v8(m+n+1 downto 1);	
		--wait for 10 ns;
		D((NI -8)*(m+n+1) downto (NI -9)*(m+n+1) + 1) <= v9(m+n+1 downto 1);	
		--wait for 10 ns;
		D((NI -9)*(m+n+1) downto (NI -10)*(m+n+1) + 1) <= v10(m+n+1 downto 1);	
		
		--wait for 10 ns;
		--D <= (others => '0');
    v1(m+n+1 downto 1) <= "111110101000";
    v2(m+n+1 downto 1) <= "000000001001";
    v3(m+n+1 downto 1) <= "101010100101";
    v4(m+n+1 downto 1) <= "111111001000";
    v5(m+n+1 downto 1) <= "111101100100";
    v6(m+n+1 downto 1) <= "001101101010";
    v7(m+n+1 downto 1) <= "111111011000";
    v8(m+n+1 downto 1) <= "000110110111";
    v9(m+n+1 downto 1) <= "111110000000";
    v10(m+n+1 downto 1)<= "000001010010";
    
    wait for 10 ns;
		D(NI*(m+n+1) downto (NI -1)*(m+n+1) + 1) <= v1(m+n+1 downto 1);		
		--wait for 10 ns;
		D((NI -1)*(m+n+1) downto (NI -2)*(m+n+1) + 1) <= v2(m+n+1 downto 1);	
	  --wait for 10 ns;
		D((NI -2)*(m+n+1) downto (NI -3)*(m+n+1) + 1) <= v3(m+n+1 downto 1);		
		--wait for 10 ns;	
		D((NI -3)*(m+n+1) downto (NI -4)*(m+n+1) + 1) <= v4(m+n+1 downto 1);	
		--wait for 10 ns;
		D((NI -4)*(m+n+1) downto (NI -5)*(m+n+1) + 1) <= v5(m+n+1 downto 1);	
		--wait for 10 ns;
		D((NI -5)*(m+n+1) downto (NI -6)*(m+n+1) + 1) <= v6(m+n+1 downto 1);	
		--wait for 10 ns;
		D((NI -6)*(m+n+1) downto (NI -7)*(m+n+1) + 1) <= v7(m+n+1 downto 1);	
		--wait for 10 ns;
		D((NI -7)*(m+n+1) downto (NI -8)*(m+n+1) + 1) <= v8(m+n+1 downto 1);	
		--wait for 10 ns;
		D((NI -8)*(m+n+1) downto (NI -9)*(m+n+1) + 1) <= v9(m+n+1 downto 1);	
		--wait for 10 ns;
		D((NI -9)*(m+n+1) downto (NI -10)*(m+n+1) + 1) <= v10(m+n+1 downto 1);
		
		                      
		v1(m+n+1 downto 1) <= "000101001001";
    v2(m+n+1 downto 1) <= "000000001001";
    v3(m+n+1 downto 1) <= "101011011101";
    v4(m+n+1 downto 1) <= "010101001000";
    v5(m+n+1 downto 1) <= "111001100100";
    v6(m+n+1 downto 1) <= "001101101000";
    v7(m+n+1 downto 1) <= "100111110100";
    v8(m+n+1 downto 1) <= "000000000111";
    v9(m+n+1 downto 1) <= "111111111000";
    v10(m+n+1 downto 1)<= "000000101001";

    wait for 10 ns;
		D(NI*(m+n+1) downto (NI -1)*(m+n+1) + 1) <= v1(m+n+1 downto 1);		
		--wait for 10 ns;
		D((NI -1)*(m+n+1) downto (NI -2)*(m+n+1) + 1) <= v2(m+n+1 downto 1);	
	  --wait for 10 ns;
		D((NI -2)*(m+n+1) downto (NI -3)*(m+n+1) + 1) <= v3(m+n+1 downto 1);		
		--wait for 10 ns;	
		D((NI -3)*(m+n+1) downto (NI -4)*(m+n+1) + 1) <= v4(m+n+1 downto 1);	
		--wait for 10 ns;
		D((NI -4)*(m+n+1) downto (NI -5)*(m+n+1) + 1) <= v5(m+n+1 downto 1);	
		--wait for 10 ns;
		D((NI -5)*(m+n+1) downto (NI -6)*(m+n+1) + 1) <= v6(m+n+1 downto 1);	
		--wait for 10 ns;
		D((NI -6)*(m+n+1) downto (NI -7)*(m+n+1) + 1) <= v7(m+n+1 downto 1);	
		--wait for 10 ns;
		D((NI -7)*(m+n+1) downto (NI -8)*(m+n+1) + 1) <= v8(m+n+1 downto 1);	
		--wait for 10 ns;
		D((NI -8)*(m+n+1) downto (NI -9)*(m+n+1) + 1) <= v9(m+n+1 downto 1);	
		--wait for 10 ns;
		D((NI -9)*(m+n+1) downto (NI -10)*(m+n+1) + 1) <= v10(m+n+1 downto 1);	
		

		v1(m+n+1 downto 1) <= "000101000101";
    v2(m+n+1 downto 1) <= "001101111110";
    v3(m+n+1 downto 1) <= "101010101101";
    v4(m+n+1 downto 1) <= "010000101000";
    v5(m+n+1 downto 1) <= "110000100100";
    v6(m+n+1 downto 1) <= "010101011100";
    v7(m+n+1 downto 1) <= "101111001111";
    v8(m+n+1 downto 1) <= "000101110011";
    v9(m+n+1 downto 1) <= "111101010100";
    v10(m+n+1 downto 1)<= "000010110101";
  
    wait for 10 ns;
		D(NI*(m+n+1) downto (NI -1)*(m+n+1) + 1) <= v1(m+n+1 downto 1);		
		--wait for 10 ns;
		D((NI -1)*(m+n+1) downto (NI -2)*(m+n+1) + 1) <= v2(m+n+1 downto 1);	
	  --wait for 10 ns;
		D((NI -2)*(m+n+1) downto (NI -3)*(m+n+1) + 1) <= v3(m+n+1 downto 1);		
		--wait for 10 ns;	
		D((NI -3)*(m+n+1) downto (NI -4)*(m+n+1) + 1) <= v4(m+n+1 downto 1);	
		--wait for 10 ns;
		D((NI -4)*(m+n+1) downto (NI -5)*(m+n+1) + 1) <= v5(m+n+1 downto 1);	
		--wait for 10 ns;
		D((NI -5)*(m+n+1) downto (NI -6)*(m+n+1) + 1) <= v6(m+n+1 downto 1);	
		--wait for 10 ns;
		D((NI -6)*(m+n+1) downto (NI -7)*(m+n+1) + 1) <= v7(m+n+1 downto 1);	
		--wait for 10 ns;
		D((NI -7)*(m+n+1) downto (NI -8)*(m+n+1) + 1) <= v8(m+n+1 downto 1);	
		--wait for 10 ns;
		D((NI -8)*(m+n+1) downto (NI -9)*(m+n+1) + 1) <= v9(m+n+1 downto 1);	
		--wait for 10 ns;
		D((NI -9)*(m+n+1) downto (NI -10)*(m+n+1) + 1) <= v10(m+n+1 downto 1);
		
      wait;
   end process;
    
end;
