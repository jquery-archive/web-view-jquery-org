<?php

class GitProxy {
	private $root 		= 'http://github.com/api/v2/json/';
	private $user 		= null;
	private $repository = null;
	private $branch 	= null;
	private $path 		= null;

	function __construct($user = null, $repository = null, $branch = null) {
		$this->setUser($user);
		$this->setRepository($repository);
	}

	public function setUser($user) {
		if ( $user != null ) {
			$this->user = $user;
		}
	}

	public function setRepository($repository) {
		if ( $repository != null ) {
			$this->repository = $repository;
		}
	}

	public function setBranch($branch) {
		if ( $branch != null ) {
			$this->branch = $branch;
		}
	}

	public function setPath($path) {
		if ( $path != null ) {
			$this->path = $path;
		}
	}

	private function url($cmd, $ref = null) {
		$url = $this->root . $cmd . '/' . $this->user;
		if ( !empty($this->repository) ) {
			$url .= '/' . $this->repository;
		}
		if ( !empty($this->branch) ) {
			$url .= '/' . $this->branch;
		}

		if ( !empty($ref) ) {
			$url .= '/' . $ref;
		}

		if ( !empty($this->path) ) {
			$url .= '/' . $this->path;
		}

		return $url;
	}

	private function cmd($cmd, $ref = null) {
		$url = $this->url($cmd, $ref);

		echo "URL: $url\n";
		$ch = curl_init();
		curl_setopt($ch, CURLOPT_URL, $url);
		curl_setopt($ch, CURLOPT_HEADER, 0);
		curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
		$payload = curl_exec($ch);
		$statusCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);

		curl_close($ch);

		if ( $statusCode == '404' ) {
			echo "404 occurred: $url\n";
			return false;
		}

		echo "Response:\n";
		var_dump($payload);

		if ( $payload !== false ) {
			return json_decode($payload);
		}
		return false;
	}

	public function listRepositories($user = null) {
		$this->setUser($user);
		$repos = $this->cmd('repos/show');
		var_dump($repos);
		if ( $repos !== false ) {
			return $repos->repositories;
		}
		return false;
		
	}

	public function repositoryInfo($repository = null) {
		$this->setRepository($repository);
		$repos = $this->cmd('repos/show');
		var_dump($repos);
		if ( $repos !== false ) {
			return $repos->repositories;
		}
		return false;
		
	}

	public function listBranches($repository = null) {
		$this->setRepository($repository);
		$ret = $this->cmd('repos/show', 'branches');
		return $ret->branches;
	}

	public function tree($branch = null) {
		$this->setBranch($branch);
		$objects = $this->cmd('tree/show');
		var_dump($objects);
	}

	public function listObjects($path = null) {
		$objects = $this->cmd('blob/all');
		var_dump($objects);
	}
}

