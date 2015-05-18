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
  generic( m  : integer := 11; 
           n  : integer := 1; 
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
    v1(m+n+1 downto 1) <= "1111100000100";
    v2(m+n+1 downto 1) <= "0000000010001";
    v3(m+n+1 downto 1) <= "0000100100000";
    v4(m+n+1 downto 1) <= "1111110011000";
    v5(m+n+1 downto 1) <= "1111101100100";
    v6(m+n+1 downto 1) <= "0000100000000";
    v7(m+n+1 downto 1) <= "1111100000000";
    v8(m+n+1 downto 1) <= "0001000001001";
    v9(m+n+1 downto 1) <= "1111010000000";
    v10(m+n+1 downto 1)<= "0000001111001";
    
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
    v1(m+n+1 downto 1) <= "1111100101000";
    v2(m+n+1 downto 1) <= "0000001001001";
    v3(m+n+1 downto 1) <= "1011011000101";
    v4(m+n+1 downto 1) <= "1111111001000";
    v5(m+n+1 downto 1) <= "1111011001100";
    v6(m+n+1 downto 1) <= "0011011010110";
    v7(m+n+1 downto 1) <= "1111111011000";
    v8(m+n+1 downto 1) <= "0001100110111";
    v9(m+n+1 downto 1) <= "1111101000000";
    v10(m+n+1 downto 1)<= "0000010110010";
    
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
		
		                      
	v1(m+n+1 downto 1) <= "0001010101001";
    v2(m+n+1 downto 1) <= "0000001001001";
    v3(m+n+1 downto 1) <= "1010011011101";
    v4(m+n+1 downto 1) <= "0101010101000";
    v5(m+n+1 downto 1) <= "1110101100100";
    v6(m+n+1 downto 1) <= "0011011011000";
    v7(m+n+1 downto 1) <= "1000111110100";
    v8(m+n+1 downto 1) <= "0000000100111";
    v9(m+n+1 downto 1) <= "1111011111000";
    v10(m+n+1 downto 1)<= "0000001011001";

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
		

	v1(m+n+1 downto 1) <= "0001111000101";
    v2(m+n+1 downto 1) <= "0011011111110";
    v3(m+n+1 downto 1) <= "1001010101101";
    v4(m+n+1 downto 1) <= "0100000101000";
    v5(m+n+1 downto 1) <= "1100000100100";
    v6(m+n+1 downto 1) <= "0101010111100";
    v7(m+n+1 downto 1) <= "1011111001111";
    v8(m+n+1 downto 1) <= "0001011100011";
    v9(m+n+1 downto 1) <= "1110101010100";
    v10(m+n+1 downto 1)<= "0000101110101";
  
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
