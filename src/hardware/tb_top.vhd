---------------------------------------------------
-- File: tb_top.vhd
-- Entity: tb_top
-- Architecture: STRUCT
-- Author: Qutaiba Saleh
-- Created: 5/6/15
-- Modified: 5/7/15
-- VHDL'93
-- Testbench for top  
----------------------------------------------------
--
LIBRARY ieee;
USE ieee.std_logic_1164.ALL;
use IEEE.STD_LOGIC_ARITH.ALL;
use IEEE.STD_LOGIC_UNSIGNED.ALL;
use std.textio.all;
use ieee.std_logic_textio.all;
use ieee.numeric_std.all;
--
entity tb_top is 
  generic (
	s  : integer := 49; -- size of the input image
    n  : integer := 11;
    m  : integer := 1
    );
end tb_top;

architecture STRUCT of tb_top is 
--
-- unit under test component decleration 
component top is 
  generic (
	s  : integer := 49; -- size of the input image
    n  : integer := 11;
    m  : integer := 1
    );
  port (
    clk        : in  std_logic;
    Label_in   : in  std_logic;
	Mode       : in std_logic_vector(1 downto 0); -- 00: Idle, 01: Reset, 10: Train, 11: Test
    pixels     : in  std_logic_vector(s*(m+n+1) downto 1);
    LFSR_init  : in  std_logic_vector(m+n downto 1);
	alpha      : in  std_logic_vector(m+n+1 downto 1);
	ready      : out std_logic;
	label_out  : out std_logic
    );
end component;
--
-- signals 
    -- inputs
    signal clk        : std_logic;
    signal Label_in   : std_logic:= '0';
	signal Mode       : std_logic_vector(1 downto 0):= "00"; 
    signal pixels     : std_logic_vector(s*(m+n+1) downto 1):=(others =>'0');
    signal LFSR_init  : std_logic_vector(m+n downto 1):=(others =>'0');
	signal alpha      : std_logic_vector(m+n+1 downto 1):="0000000000010";
    -- outputs 
    signal ready      : std_logic;
	signal label_out  : std_logic;
	--
    type one_d_memory  is array( 1 to s) of std_logic_vector(m+n+1 downto 1);
    type two_d_memory  is array( 1 to 1000) of one_d_memory;
-- constants
	constant clk_period   : time    := 10 ns;
	constant train_length : integer := 800;
	constant test_length  : integer := 200;
	constant epoch        : integer := 1;
--
begin
  --
  -- instantiate the unit under test 
  uut: top
    generic map ( 
                  s => s,
                  m  => m,
                  n  => n
                  )
    port map (
		clk        => clk,
		Label_in   => Label_in,
		Mode       => Mode,
		pixels     => pixels,
		LFSR_init  => LFSR_init,
		alpha      => alpha,
		ready      => ready,
		label_out  => label_out
      );
  --
  clk_process :process
   begin
		clk <= '0';
		wait for clk_period/2;
		clk <= '1';
		wait for clk_period/2;
   end process;
 
  sim_proc: process
	  -- files decleration
	  file f_train_vectors   : text open read_mode is "train.txt"; ---- input training vectors 
	  file f_test_vectors    : text open read_mode is "test.txt"; ---- input testing vectors 
	  file f_test_out        : text open write_mode is "test_output.txt"; ---- results of test vectors
    -- variables 
    variable in_line         : line;
	variable out_line        : line;
	variable end_of_line     : boolean;
	variable label_value     : std_logic;
	variable pixel_value     : std_logic_vector(m+n+1 downto 1);
	--
	variable train_in        : two_d_memory := (others => (others => (others => '0')));
	variable test_in         : two_d_memory := (others => (others => (others => '0')));
	
	variable train_label     : std_logic_vector(train_length downto 1):=(others => '0');
	variable test_label      : std_logic_vector(test_length downto 1):=(others => '0');
		
	variable i : integer:=1;
	variable j : integer:=1;
	variable k : integer:=1;
	
		
		
   begin		
     
     
    -------------------------------------------------------------
    -- read input and output TRAINING vectors ---
    -------------------------------------------------------------
    while not endfile(f_train_vectors) loop
		readline(f_train_vectors,in_line); -------------------------- read first line  
		read(in_line,label_value,end_of_line); ------ read first value of the current line
		train_label(i) := label_value;
		read(in_line,pixel_value,end_of_line); ------ read the first pixel value
		while end_of_line loop
			train_in(i)(j)(m+n+1 downto 1) := pixel_value;
			read(in_line,pixel_value,end_of_line);
			j := j + 1;
		end loop;
		j := 1;
		i := i + 1;
	end loop;
	-------------------------------------------------------------
    -- read input and output TESTING vectors ---
    -------------------------------------------------------------
	i := 1;
	j := 1;
    while not endfile(f_test_vectors) loop
		readline(f_test_vectors,in_line); -------------------------- read first line  
		read(in_line,label_value,end_of_line); ------ read first value of the current line
		test_label(i) := label_value;
		read(in_line,pixel_value,end_of_line); ------ read the first pixel value
		while end_of_line loop
			test_in(i)(j)(m+n+1 downto 1) := pixel_value;
			read(in_line,pixel_value,end_of_line);
			j := j + 1;
		end loop;
		j := 1;
		i := i + 1;
	end loop;
	
	-------------------------------------------------------------
    -- Reset and weight initialization  ---
    -------------------------------------------------------------
	LFSR_init <= "000000000001";
	Mode <= "01";
	wait for 2*clk_period;
	Mode <= "00";
	wait until ready = '1';
	wait for 2*clk_period;
    -------------------------------------------------------------
    -- TRAINING  ---
    -------------------------------------------------------------
	Mode <= "10";
	wait for 2*clk_period;
	for k in 1 to epoch loop
		for i in 1 to train_length loop
			for j in 1 to s loop
				pixels(j*(m+n+1) downto (j-1)*(m+n+1)+1) <= train_in(i)(j);
			end loop;
			Label_in <= train_label(i);
			wait for clk_period;
		end loop;
	end loop;
	Mode <= "00";
	wait for 2*clk_period;
	-------------------------------------------------------------
    -- TESTING  ---
    -------------------------------------------------------------
	Mode <= "11";
	wait for 2*clk_period;
	for i in 1 to test_length loop
		for j in 1 to s loop
			pixels(j*(m+n+1) downto (j-1)*(m+n+1)+1) <= test_in(i)(j);
		end loop;
		wait for 16*clk_period;
		test_label(i) := label_out;
	end loop;
	Mode <= "00";
	wait for 2*clk_period;
    wait;
   end process;
end;