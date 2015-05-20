---------------------------------------------------
-- File: weight_block.vhd
-- Entity: weight_block
-- Architecture: STRUCT
-- Author: Qutaiba Saleh
-- Created: 5/5/15
-- Modified: 5/5/15
-- VHDL'93
-- Description: weight_block
----------------------------------------------------
--
LIBRARY ieee;
USE ieee.std_logic_1164.ALL;
--
entity weight_block is 
  generic (
	s  : integer;
    n  : integer;
    m  : integer
    );
  port (
    clk        		 : in  std_logic;
	Label_in   		 : in  std_logic;
    reset_flag 		 : in  std_logic;
	train_flag 		 : in  std_logic;
	test_flag  		 : in  std_logic;
	
	LFSR_in   		 : in  std_logic_vector(m+n+1 downto 1);
	train_in  		 : in  std_logic_vector(s*(m+n+1) downto 1);
	
	LFSR_out   		 : out std_logic_vector(m+n+1 downto 1);
	weight_train_out : out std_logic_vector(s*(m+n+1) downto 1);
	weight_test_out  : out std_logic_vector(s*(m+n+1) downto 1)
    );
end weight_block;
-- 
architecture STRUCT of weight_block is
	-- component of one register that contains only one weight value 
	component one_weight is 
	  generic (
		n  : integer;
		m  : integer
		);
	  port (
		clk        		 : in  std_logic;
		Label_in   		 : in  std_logic;
		reset_flag 		 : in  std_logic;
		train_flag 		 : in  std_logic;
		test_flag  		 : in  std_logic;
		
		LFSR_in    		 : in  std_logic_vector(m+n+1 downto 1);
		train_in   		 : in  std_logic_vector(m+n+1 downto 1);
		
		LFSR_out    	 : out std_logic_vector(m+n+1 downto 1);
		weight_train_out : out std_logic_vector(m+n+1 downto 1);
		weight_test_out  : out std_logic_vector(m+n+1 downto 1)
		);
	end component;
	-- connection signal 
	--type connection  is array( 0 to s) of std_logic_vector(m+n+1 downto 1);
	--signal sLFSR : connection;
	signal sLFSR : std_logic_vector((s+1)*(m+n+1) downto 1);
	
begin
	-- connect the terminal connection signals to the first LFSR_in and the last LFSR_out
	--sLFSR(0) <= LFSR_in;
	--LFSR_out <= sLFSR(s);
	sLFSR((m+n+1) downto 1) <= LFSR_in;
	LFSR_out <= sLFSR((s+1)*(m+n+1) downto s*(m+n+1)+1);
	-- Generate weight registers
	weight_gen: for i in 1 to s generate
		weight_reg: one_weight
			generic map (m => m, n => n)
			port map (
				clk        => clk,
				Label_in   => Label_in,
				reset_flag => reset_flag,
				train_flag => train_flag,
				test_flag  => test_flag,
				
				LFSR_in    => sLFSR(i*(m+n+1) downto (i-1)*(m+n+1)+1),
				train_in   => train_in(i*(m+n+1) downto (i-1)*(m+n+1)+1),
				
				LFSR_out   => sLFSR((i+1)*(m+n+1) downto i*(m+n+1)+1),
				weight_train_out => weight_train_out(i*(m+n+1) downto (i-1)*(m+n+1)+1),
				weight_test_out  => weight_test_out(i*(m+n+1) downto (i-1)*(m+n+1)+1)
			);
		end generate;    

end architecture;